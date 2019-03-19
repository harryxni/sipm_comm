#!/usr/bin/env python3
import serial
import io
from pyfiglet import Figlet

f=Figlet(font='slant')

sr=serial.Serial(port='/dev/ttyACM0', baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
print(f.renderText('ArduSiPM'))
x=1
#sr.write(b'm')
while (x==1):
    print(sr.readline().strip())




