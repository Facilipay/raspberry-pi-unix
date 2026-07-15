# Raspberry Pi UNIX Clock

Displays the UNIX timestamp and current time on a 20x4 LCD screen.

## Hardware
- Raspberry Pi 3
- 20x4 LCD screen (RoHS 2004A)
- Adafruit USB & Serial RGB Character LCD Backpack

## Installation
pip3 install pyserial

## Usage
python3 clock.py

## Auto-start on boot
Add this line in /etc/rc.local before exit 0 :
python3 /home/pi/clock.py &

## Note
Set the time manually after each reboot :
sudo date -s "YYYY-MM-DD HH:MM:SS"
