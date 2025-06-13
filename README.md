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
  - Aufnahme kann vorzeitig abgebrochen werden
- **libcamera-still** für Bilder
 - **FFmpeg** für FHD-Videos (30 FPS)
- **systemd**-Service für Autostart
- Fortlaufend nummerierte Ordner und Videos

## Voraussetzungen

- Raspberry Pi Zero 2 W mit Camera Module 3
- Raspbian (aktuell)
- Internetzugang einmalig zur Installation
- Keine integrierte RTC – ohne Internet zeigt die Uhrzeit standardmäßig falsch an

## Installation

Für die Schnellinstallation gibt es ein Skript, das zunächst dieses
Repository klont und danach `install.sh` aufruft. Es reicht also, den
folgenden Befehl auszuführen:

```bash
curl -sL https://raw.githubusercontent.com/philippxmeyer/RaspiZeroCam/main/install-oneclick.sh | bash
```

Nach Abschluss empfiehlt sich ein Neustart des Pi, damit Hotspot und Webdienst
laufen. Das Skript installiert dabei `authbind`, richtet die nötigen
Berechtigungen ein und erlaubt so dem Flask-Server, weiterhin als Benutzer
`pi` auf Port 80 zu lauschen.

Wer das Repository bereits geklont hat, kann die Installation auch direkt
per

```bash
./install.sh
```

## Benutzung

1. Den Pi nach der Installation starten. Er richtet den WLAN-Hotspot
   `PiZero_AP` mit dem Passwort `Timelapse123` ein.
2. Mit einem WLAN-fähigen Gerät (Smartphone, Laptop, Tablet) diesem Netz
   beitreten.
3. Im Browser `http://192.168.4.1` aufrufen. Die Weboberfläche zeigt eine
   Live-Vorschau der Kamera und Eingabefelder für das Timelapse-Intervall,
   die Gesamtdauer sowie ISO und Fokus. Die Dauer wird im Format
   `hh:mm:ss` angegeben.
4. Gewünschte Werte eintragen und auf **Aufnahme starten** klicken. Während
   der Aufnahme ist die Schaltfläche deaktiviert.
5. Läuft eine Aufnahme, kann sie über **Aufnahme abbrechen** vorzeitig beendet
   werden. Anschließend lässt sich entscheiden, ob aus den vorhandenen Bildern
   ein Video gerendert oder alles verworfen wird.
6. Nach Abschluss erscheint das erzeugte Video unter *Fertige Videos* und
   kann direkt heruntergeladen werden. Die Datei wird auch auf dem Pi unter
   `/home/pi/timelapse/videos` gespeichert.
   Bilder und Videos erhalten fortlaufende Nummern (0001, 0002, ...).
