#!/bin/bash
# Copy network configuration files to their system locations
sudo cp network-config/dhcpcd.conf /etc/dhcpcd.conf
sudo cp network-config/hostapd.conf /etc/hostapd/hostapd.conf
sudo cp network-config/dnsmasq.conf /etc/dnsmasq.conf
