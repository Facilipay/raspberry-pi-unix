import serial
import time

lcd = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

reset     = bytearray([0xFE, 0x58])
no_scroll = bytearray([0xFE, 0x52])
no_cursor = bytearray([0xFE, 0x4B])
line1     = bytearray([0xFE, 0x47, 0x01, 0x01])
line2     = bytearray([0xFE, 0x47, 0x01, 0x02])

lcd.write(reset)
time.sleep(0.5)
lcd.write(no_scroll)
time.sleep(0.1)
lcd.write(no_cursor)
time.sleep(0.1)

while True:
    unix  = f"UNIX:{int(time.time()):,}".ljust(20)
    heure = time.strftime("%Hh %Mm %Ss").center(20)

    lcd.write(line1)
    lcd.write(unix.encode())
    lcd.write(line2)
    lcd.write(heure.encode())

    time.sleep(1)
