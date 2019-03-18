#!/usr/bin/env python3
import serial

serialPort=serial.Serial(port='COM4', baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

