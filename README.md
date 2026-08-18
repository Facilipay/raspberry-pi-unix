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
sudo apt install python3-serial

(On current Raspberry Pi OS (Bookworm), plain "pip3 install pyserial" is refused
with an "externally-managed-environment" error — the apt package is the simplest
way to install it system-wide, which is what the boot service needs.)

## Step 4 - Copy the files
Copy clock.py and clock.service to /home/pi/ on the Raspberry Pi.

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
Copy the provided systemd service file and enable it :
sudo cp clock.service /etc/systemd/system/clock.service
sudo systemctl enable --now clock

The service starts the clock at every boot and restarts it automatically if it
ever crashes (e.g. the LCD is unplugged and replugged, or the USB port is not
ready yet when the Pi boots).

(rc.local is deprecated and no longer runs by default on current Raspberry Pi
OS, and it would not restart the script if it crashed.)

## Display
Line 1 : Irish local time in 12-hour format (e.g. Irish 04:27:39 PM)
Line 2 : UNIX timestamp (e.g. UNIX:1,787,066,859)

The time is rendered in the Europe/Dublin timezone explicitly, not in whatever
timezone the Pi happens to be set to, so it stays correct after a re-image.
Irish summer time is handled by the timezone database, so the hour is right on
both sides of the March and October changeovers with no code change.

The IST/GMT suffix is deliberately not shown: "Irish 04:27:39 PM IST" is 21
characters and the panel is 20 wide, so the explicit "Irish" label takes its
place.

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
- The script normally finds the LCD by its USB ID (239a:0001) whatever the port
  name, so a wrong port should not happen. To double check, list the ports :
  ls /dev/ttyACM*
- Check the baud rate is 9600 (default in clock.py).

### "Permission denied" on /dev/ttyACM0
- Your user is not allowed to use the serial port. Add it to the dialout group, then log out and back in :
  sudo usermod -a -G dialout $USER

### "No module named serial"
- pyserial is missing. Install it :
  sudo apt install python3-serial

### The time is wrong
- Check the time sync (see Step 5) :
  timedatectl status
  It must show "System clock synchronized: yes". If not, the Pi has no network — give it WiFi or a phone hotspot and reboot.
- The Pi 3 has no battery clock, so a wrong time after a power cut is normal until it syncs.

### The clock does not start automatically on boot
- Check the service status and its recent logs :
  systemctl status clock
- Make sure it is enabled :
  sudo systemctl enable clock
- Confirm the script path is correct :
  ls /home/pi/clock.py

### Check whether the script is running
  systemctl status clock
- To stop it :
  sudo systemctl stop clock
- To stop it permanently (no restart at boot) :
  sudo systemctl disable --now clock
