#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, \
                  send_from_directory, Response
import subprocess, threading, os, logging, time

app = Flask(__name__)
BASE = '/home/pi/timelapse'
IMG_DIR = os.path.join(BASE, 'images')
VID_DIR = os.path.join(BASE, 'videos')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VID_DIR, exist_ok=True)

# Einfaches Logging zur Fehlersuche
logging.basicConfig(
    filename=os.path.join(BASE, 'timelapse.log'),
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

# Libcamera wird für die Vorschau erst bei Bedarf genutzt

capturing = False
capture_process = None
capture_info = {}
abort_requested = False


def next_run_number():
    existing = [d for d in os.listdir(IMG_DIR)
                if os.path.isdir(os.path.join(IMG_DIR, d))]
    nums = [int(d) for d in existing if d.isdigit()]
    next_num = max(nums) + 1 if nums else 1
    return f"{next_num:04d}"

@app.route('/', methods=['GET', 'POST'])
def index():
    global capturing
    if request.method == 'POST' and not capturing:
        try:
            spf = float(request.form['seconds_per_frame'])
            dur_str = request.form['duration']
            parts = dur_str.split(':')
            if len(parts) == 2:
                h, m = parts
                dur = int(h) * 3600 + int(m) * 60
            elif len(parts) == 3:
                h, m, s = parts
                dur = int(h) * 3600 + int(m) * 60 + int(s)
            else:
                raise ValueError
            if spf <= 0 or dur <= 0:
                raise ValueError
        except (ValueError, KeyError):
            return redirect(url_for('index'))

        iso = request.form['iso']
        focus = request.form['focus']
        threading.Thread(
            target=capture, args=(spf, dur, iso, focus), daemon=True
        ).start()
        capturing = True
        return redirect(url_for('index'))
    videos = sorted(f for f in os.listdir(VID_DIR) if f.endswith('.mp4'))
    return render_template('index.html', videos=videos, capturing=capturing)

@app.route('/preview')
def preview():
    def gen():
        while True:
            if capturing:
                break
            frame = subprocess.check_output([
                'libcamera-still', '-n', '--immediate', '-o', '-', '--width', '640', '--height', '360']
            )
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(VID_DIR, filename, as_attachment=True)

@app.route('/cancel', methods=['POST'])
def cancel():
    global capturing, abort_requested, capture_process, capture_info
    if capturing and capture_process:
        abort_requested = True
        capture_process.terminate()
        capturing = False
        img_dir = capture_info.get('dir')
        img_count = 0
        if img_dir and os.path.exists(img_dir):
            img_count = len([f for f in os.listdir(img_dir) if f.endswith('.jpg')])
        if img_count > 0:
            return render_template('cancel.html', images=img_count)
    return redirect(url_for('index'))

@app.route('/cancel_action', methods=['POST'])
def cancel_action():
    action = request.form.get('action')
    if action == 'render' and capture_info.get('dir'):
        try:
            render_video(capture_info['dir'], capture_info['fps'], capture_info['run'])
        except subprocess.CalledProcessError:
            pass
    elif action == 'discard' and capture_info.get('dir'):
        for f in os.listdir(capture_info['dir']):
            if f.endswith('.jpg'):
                os.remove(os.path.join(capture_info['dir'], f))
    return redirect(url_for('index'))

def render_video(img_dir, fps, run_num):
    video_file = os.path.join(VID_DIR, f'{run_num}.mp4')
    subprocess.run([
        'ffmpeg','-y','-r',str(fps),
        '-pattern_type','glob','-i',os.path.join(img_dir,'*.jpg'),
        '-vf','scale=1920:1080','-c:v','libx264','-pix_fmt','yuv420p',
        video_file
    ], check=True)

def capture(seconds_per_frame, duration, iso, focus):
    global capturing, capture_process, capture_info, abort_requested
    if seconds_per_frame <= 0 or duration <= 0:
        capturing = False
        return
    # give the preview generator time to exit and free the camera
    time.sleep(1)
    run_num = next_run_number()
    out = os.path.join(IMG_DIR, run_num)
    os.makedirs(out, exist_ok=True)

    ms_per = int(seconds_per_frame * 1000)
    us_per = ms_per * 1000

    shutter_args = [
        '--shutter', str(us_per),
        '--exposure', 'normal'
    ]

    iso_args = ['--gain', str(int(int(iso)/100))] if iso!='auto' else []
    if focus=='auto':
        focus_args=['--autofocus-mode','auto','--autofocus-on-capture']
    else:
        focus_args=['--autofocus-mode','manual','--lens-position','0.0']

    cmd = [
        'libcamera-still',
        '--timelapse', str(ms_per),
        '--timeout', str(int(duration*1000)),
        '-o', os.path.join(out, 'img_%04d.jpg')
    ] + shutter_args + iso_args + focus_args

    capture_info = {'dir': out, 'fps': 1/seconds_per_frame, 'run': run_num}
    abort_requested = False
    try:
        logging.info("Starting capture: %s", ' '.join(cmd))
        capture_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        stdout, stderr = capture_process.communicate()
        if stdout:
            logging.info(stdout.decode(errors='ignore'))
        if stderr:
            logging.error(stderr.decode(errors='ignore'))
        logging.info("Capture exited with code %s", capture_process.returncode)
    finally:
        capture_process = None
        capturing = False
    if not abort_requested:
        render_video(capture_info['dir'], capture_info['fps'], capture_info['run'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
