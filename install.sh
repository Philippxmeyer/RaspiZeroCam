#!/bin/bash
set -e

# Install required packages
sudo apt install -y hostapd dnsmasq python3-flask libcamera-apps ffmpeg authbind

# Copy network configuration files
sudo cp network-config/dhcpcd.conf /etc/dhcpcd.conf
sudo cp network-config/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp network-config/dnsmasq.conf /etc/dnsmasq.conf

# Enable hotspot services
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq

# Allow user 'pi' to bind to port 80 using authbind
sudo touch /etc/authbind/byport/80
sudo chown pi /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80

# Copy application files
sudo mkdir -p /home/pi/timelapse
sudo cp -r timelapse/* /home/pi/timelapse/

# Install systemd service
sudo cp systemd/timelapse.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable timelapse.service

# Clean up apt caches
sudo apt clean

echo "Installation abgeschlossen. Jetzt neu starten."
