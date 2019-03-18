#!/usr/bin/env python3
import serial
import io

sr=serial.Serial(port='/dev/ttyACM0', baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
x=1
while (x==1):
    print(sr.readline())




