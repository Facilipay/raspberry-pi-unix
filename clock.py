import serial
import serial.tools.list_ports
import time

LCD_VID = 0x239A
LCD_PID = 0x0001


def find_lcd_port():
    for port in serial.tools.list_ports.comports():
        if port.vid == LCD_VID and port.pid == LCD_PID:
            return port.device
    return '/dev/ttyACM0'


lcd = serial.Serial(find_lcd_port(), 9600, write_timeout=2)
time.sleep(2)

clear           = bytearray([0xFE, 0x58])
no_scroll       = bytearray([0xFE, 0x52])
no_cursor       = bytearray([0xFE, 0x4B])
no_block_cursor = bytearray([0xFE, 0x54])
line1           = bytearray([0xFE, 0x47, 0x01, 0x01])
line2           = bytearray([0xFE, 0x47, 0x01, 0x02])

lcd.write(clear)
time.sleep(0.5)
lcd.write(no_scroll)
time.sleep(0.1)
lcd.write(no_cursor)
time.sleep(0.1)
lcd.write(no_block_cursor)
time.sleep(0.1)

try:
    while True:
        unix_line = f"UNIX:{int(time.time()):,}".ljust(20)
        time_line = time.strftime("%Hh %Mm %Ss").center(20)

        lcd.write(line1)
        lcd.write(unix_line.encode())
        lcd.write(line2)
        lcd.write(time_line.encode())

        # sleep to the next second boundary so the display never skips a second
        time.sleep(1 - time.time() % 1)
finally:
    lcd.close()
