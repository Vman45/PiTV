#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install major dependencies
sudo apt install python3 steamlink

# Install python dependencies
pip3 install pynput flask

#Install media chromium
curl -fsSL https://pi.vpetkov.net -o ventz-media-pi
sh ventz-media-pi

# Download python script
mkdir /home/pi/Documents/PiTV
cd /home/pi/Documents/PiTV
wget https://raw.githubusercontent.com/jnstockley/PiTV/master/PiTV.py

# Download optional dependencies
cd ~
wget -O urserver.deb http://www.unifiedremote.com/d/rpi-deb
sudo dpkg -i urserver.deb

# Auto run pyhton script
mkdir /home/pi/.config/autostart || echo "Autostart folder exists"
echo "[Desktop Entry]
Type=Application
Name=PiTV
Exec=/usr/bin/python3 /home/pi/Documents/PiTV/PiTV.py
" >> /home/pi/.config/autostart/PiTV.desktop

# Start urserver
/opt/urserver/urserver-start

# Informs user to reboot
echo "Please reboot your Raspberry Pi!"
