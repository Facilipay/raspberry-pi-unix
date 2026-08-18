import time
from datetime import datetime
from zoneinfo import ZoneInfo

import serial
import serial.tools.list_ports

LCD_VID = 0x239A
LCD_PID = 0x0001
LCD_COLS = 20

# Display Dublin time explicitly rather than relying on the system timezone,
# so the clock is correct even if the Pi is re-imaged or moved elsewhere.
DUBLIN = ZoneInfo("Europe/Dublin")


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

# Rows 1 and 3 never change, so write them once instead of re-sending 40 bytes
# every second. If the backpack is power-cycled the script exits and systemd
# restarts it, which runs this setup again.
lcd.write(row1)
lcd.write(fit("Irish Local Time").encode())
lcd.write(row3)
lcd.write((" " * LCD_COLS).encode())

try:
    while True:
        now = datetime.now(DUBLIN)

        # Derive AM/PM directly rather than with %p, which renders empty under
        # some locales and would silently drop the meridiem from the panel.
        meridiem = "AM" if now.hour < 12 else "PM"

        time_line = fit(f"{now.strftime('%I:%M:%S')} {meridiem}")
        unix_line = fit(f"{int(now.timestamp()):,}")

        lcd.write(row2)
        lcd.write(time_line.encode())
        lcd.write(row4)
        lcd.write(unix_line.encode())

        # sleep to the next second boundary so the display never skips a second
        time.sleep(1 - time.time() % 1)
finally:
    lcd.close()
