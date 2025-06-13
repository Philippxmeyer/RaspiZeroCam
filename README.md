# Pi Zero 2 W Timelapse Controller

Dieses Repo richtet deinen Raspberry Pi Zero 2 W als WLAN-Hotspot ein, startet beim Boot einen Flask-Webserver für Timelapse-Aufnahmen mit Camera Module 3 und bietet Live-Preview sowie Download fertiger Videos.

## Features

- **WLAN-Hotspot** (SSID `PiZero_AP`, Passwort `Timelapse123`)
- **Flask-Web-UI** für:
  - Intervall und Dauer
  - ISO-Auswahl (Auto, 100, 200, 400, 800)
  - Fokus (Auto, Unendlich)
  - Live-Vorschau (MJPEG)
  - Download fertiger Videos
- **libcamera-still** für Bilder
- **FFmpeg** für FHD-Videos
- **systemd**-Service für Autostart

## Voraussetzungen

- Raspberry Pi Zero 2 W mit Camera Module 3
- Raspbian (aktuell)
- Internetzugang einmalig zur Installation

## Installation

1. **System updaten & Pakete installieren**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install hostapd dnsmasq python3-flask python3-opencv \
                    libcamera-apps ffmpeg
   pip3 install picamera2
```

2. **Konfigurationsdateien kopieren**
   ```bash
   ./install-network.sh
   ```
