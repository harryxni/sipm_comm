#!/usr/bin/env python3
import serial
import io

serialPort=serial.Serial(port='/dev/ttyACM0', baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)





print(serialPort.readline())




