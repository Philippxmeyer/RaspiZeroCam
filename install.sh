#!/bin/bash
set -e

# Install required packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y hostapd dnsmasq python3-flask libcamera-apps ffmpeg

# Copy network configuration files
sudo cp network-config/dhcpcd.conf /etc/dhcpcd.conf
sudo cp network-config/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp network-config/dnsmasq.conf /etc/dnsmasq.conf

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
