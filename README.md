# Raspberry Pi UNIX Clock

A minimal UNIX timestamp clock displayed on a 20x4 LCD screen, running on a Raspberry Pi 3.

## Hardware Required
- Raspberry Pi 3
- 20x4 LCD screen (RoHS 2004A)
- Adafruit USB & Serial RGB Character LCD Backpack
- Mini-USB to USB-A cable

## Step 1 - Flash the Raspberry Pi
Download and install Raspberry Pi Imager from raspberrypi.com/software.
Flash Raspberry Pi OS Lite (64-bit) on your SD card.
In the settings, enable SSH and set a username and password.

## Step 2 - Connect the LCD
Plug the mini-USB cable from the LCD backpack directly into one of the 4 USB ports on the Raspberry Pi (not via a hub).
The LCD should light up when the Raspberry Pi is powered on.
Check that it is detected by running :
lsusb
You should see a device with ID 239a:0001.

## Step 3 - Install dependencies
pip3 install pyserial

## Step 4 - Copy the script
Copy clock.py to /home/pi/clock.py on the Raspberry Pi.

## Step 5 - Set the time
The Raspberry Pi has no RTC battery, so set the time manually after each reboot :
sudo date -s "YYYY-MM-DD HH:MM:SS"

## Step 6 - Run the script
python3 clock.py

## Step 7 - Auto-start on boot
Edit /etc/rc.local :
sudo nano /etc/rc.local
Add this line before exit 0 :
python3 /home/pi/clock.py &
The script will now launch automatically every time the Raspberry Pi boots.

## Display
Line 1 : UNIX timestamp (e.g. UNIX:1,747,123,456)
Line 2 : Current time (e.g. 15h 22m 07s)
