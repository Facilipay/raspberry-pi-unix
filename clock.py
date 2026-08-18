import time
from datetime import datetime, timezone

from zoneinfo import ZoneInfo

import serial
import serial.tools.list_ports

LCD_VID = 0x239A
LCD_PID = 0x0001
LCD_COLS = 20

# Render each city's time from its own zone explicitly rather than relying on
# the system timezone, so the clock is correct wherever the Pi is set up.
# "Hungarian Local Time" is exactly 20 characters, the full panel width.
ZONES = (
    ("Irish Local Time", ZoneInfo("Europe/Dublin")),
    ("Hungarian Local Time", ZoneInfo("Europe/Budapest")),
)
TOGGLE_SECONDS = 15


def find_lcd_port():
    for port in serial.tools.list_ports.comports():
        if port.vid == LCD_VID and port.pid == LCD_PID:
            return port.device
    return '/dev/ttyACM0'


def fit(text, align=str.center):
    """Pad to the panel width, and never overflow onto the next row."""
    return align(text, LCD_COLS)[:LCD_COLS]


lcd = serial.Serial(find_lcd_port(), 9600, write_timeout=2)
time.sleep(2)

clear           = bytearray([0xFE, 0x58])
no_scroll       = bytearray([0xFE, 0x52])
no_cursor       = bytearray([0xFE, 0x4B])
no_block_cursor = bytearray([0xFE, 0x54])

# 0xFE 0x47 col row — the panel is 20x4, so rows run 1..4.
row1 = bytearray([0xFE, 0x47, 0x01, 0x01])
row2 = bytearray([0xFE, 0x47, 0x01, 0x02])
row3 = bytearray([0xFE, 0x47, 0x01, 0x03])
row4 = bytearray([0xFE, 0x47, 0x01, 0x04])

lcd.write(clear)
time.sleep(0.5)
lcd.write(no_scroll)
time.sleep(0.1)
lcd.write(no_cursor)
time.sleep(0.1)
lcd.write(no_block_cursor)
time.sleep(0.1)

# Row 3 is always blank, so write it once instead of re-sending it every
# second. If the backpack is power-cycled the script exits on the next write
# and systemd restarts it, which runs this setup again.
lcd.write(row3)
lcd.write((" " * LCD_COLS).encode())

shown_label = None

try:
    while True:
        now_utc = datetime.now(timezone.utc)
        epoch = int(now_utc.timestamp())

        # Dividing epoch seconds picks the zone, so the swap lands on :00, :15,
        # :30 and :45 rather than drifting from whenever the script started.
        label, zone = ZONES[epoch // TOGGLE_SECONDS % len(ZONES)]
        now = now_utc.astimezone(zone)

        # Derive AM/PM directly rather than with %p, which renders empty under
        # some locales and would silently drop the meridiem from the panel.
        meridiem = "AM" if now.hour < 12 else "PM"

        # The label only changes on a swap; no need to redraw it every second.
        if label != shown_label:
            lcd.write(row1)
            lcd.write(fit(label).encode())
            shown_label = label

        lcd.write(row2)
        lcd.write(fit(f"{now.strftime('%I:%M:%S')} {meridiem}").encode())
        lcd.write(row4)
        lcd.write(fit(f"{epoch:,}").encode())

        # sleep to the next second boundary so the display never skips a second
        time.sleep(1 - time.time() % 1)
finally:
    lcd.close()
