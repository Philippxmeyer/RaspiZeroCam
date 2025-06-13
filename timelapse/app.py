#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, \
                  send_from_directory, Response
from picamera2 import Picamera2
import cv2, subprocess, threading, datetime, os

app = Flask(__name__)
BASE = '/home/pi/timelapse'
IMG_DIR = os.path.join(BASE, 'images')
VID_DIR = os.path.join(BASE, 'videos')
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(VID_DIR, exist_ok=True)

# Picamera2 für Live-Preview starten
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"size": (640, 360)})
picam2.configure(preview_config)
picam2.start()

capturing = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global capturing
    if request.method == 'POST' and not capturing:
        try:
            spf = float(request.form['seconds_per_frame'])
            dur = float(request.form['duration'])
            if spf <= 0 or dur <= 0:
                raise ValueError
        except ValueError:
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
            frame = picam2.capture_array("main")
            ret, buf = cv2.imencode('.jpg', frame)
            if not ret: continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(VID_DIR, filename, as_attachment=True)

def capture(seconds_per_frame, duration, iso, focus):
    global capturing
    if seconds_per_frame <= 0 or duration <= 0:
        capturing = False
        return
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    out = os.path.join(IMG_DIR, f'tl_{ts}')
    os.makedirs(out, exist_ok=True)

    ms_per = int(seconds_per_frame * 1000)
    us_per = ms_per * 1000

    shutter_args = [
        '--shutter', str(us_per),
        '--exposure-mode', 'normal'
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

    try:
        subprocess.run(cmd, check=True)

        fps = 1/seconds_per_frame
        video_file = os.path.join(VID_DIR, f'tl_{ts}.mp4')
        subprocess.run([
            'ffmpeg','-y','-r',str(fps),
            '-pattern_type','glob','-i',os.path.join(out,'*.jpg'),
            '-vf','scale=1920:1080','-c:v','libx264','-pix_fmt','yuv420p',
            video_file
        ], check=True)
    finally:
        capturing = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
