#!/usr/bin/env python3
import serial
import sys

if len(sys.argv)<2:
    port=input('ArduSiPM Port Name: ')
else:
    port=sys.argv[1]

sr=None
while(sr is None):
    try:
        sr=setSer(port)
    except:
        print('Device not found.')
        port=input('Please Enter the Port: ')
        sr=None
        
def changeHV(value):
    pass
def rawSerial(value):
    pass
def countRate(time):
    pass


