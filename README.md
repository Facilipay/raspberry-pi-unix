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

## Step 5 - Keep the time in sync (NTP)
The Raspberry Pi 3 has no RTC battery, so it forgets the time when unplugged.
Instead of setting it by hand, let it re-sync automatically from the internet at each boot.
The Pi only needs a network connection for a few seconds at startup (home WiFi, or a phone hotspot).

Enable automatic time sync :
sudo timedatectl set-ntp true

Check that it worked (should show "System clock synchronized: yes" and "NTP service: active") :
timedatectl status

From now on, every time the Pi boots with a network available it sets the correct time on its own — no manual step needed.
If it ever boots with no network, the time will be wrong until it gets one; it self-corrects as soon as a connection is back.

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

## Troubleshooting

### The LCD does not light up
- Make sure the mini-USB cable is a real data cable, not a power-only one.
- Plug it directly into a USB port on the Pi, never through a hub.
- Try another of the 4 USB ports.

### lsusb does not show 239a:0001
- The LCD backpack is not detected. Re-seat the USB cable and reboot :
  sudo reboot
- If it still does not appear, the cable or the backpack is faulty.

### The LCD lights up but shows nothing (or garbage)
- Wrong serial port. List the available ports :
  ls /dev/ttyACM*
  If you see /dev/ttyACM1 instead of ttyACM0, edit clock.py and change the port on line 4.
- Check the baud rate is 9600 (default in clock.py).

### "Permission denied" on /dev/ttyACM0
- Your user is not allowed to use the serial port. Add it to the dialout group, then log out and back in :
  sudo usermod -a -G dialout $USER

### "No module named serial"
- pyserial is missing. Install it :
  pip3 install pyserial

### The time is wrong
- Check the time sync (see Step 5) :
  timedatectl status
  It must show "System clock synchronized: yes". If not, the Pi has no network — give it WiFi or a phone hotspot and reboot.
- The Pi 3 has no battery clock, so a wrong time after a power cut is normal until it syncs.

### The clock does not start automatically on boot
- Check that /etc/rc.local is executable :
  sudo chmod +x /etc/rc.local
- Make sure the line "python3 /home/pi/clock.py &" is placed BEFORE "exit 0".
- Confirm the script path is correct :
  ls /home/pi/clock.py

### Check whether the script is running
  ps aux | grep clock.py
- To stop it :
  sudo pkill -f clock.py
