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

Für die Schnellinstallation gibt es ein Skript, das zunächst dieses
Repository klont und danach `install.sh` aufruft. Es reicht also, den
folgenden Befehl auszuführen:

```bash
curl -sL https://raw.githubusercontent.com/USERNAME/RaspiZeroCam/main/install-oneclick.sh | bash
```

Nach Abschluss empfiehlt sich ein Neustart des Pi, damit Hotspot und Webdienst
laufen.

Wer das Repository bereits geklont hat, kann die Installation auch direkt 
per

```bash
./install.sh
```
