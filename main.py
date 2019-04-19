#!/usr/bin/env python3
import serial
import io
from pyfiglet import Figlet
import sys
f=Figlet(font='univers')
print(f.renderText('ArduSiPM'))
import serialScripts as ss

#Main.py handles most of the command line input/output 

if len(sys.argv)<2:
    port=input('ArduSiPM Port Name: ')
else:
    port=sys.argv[1]

sipm1=ss.ArduSiPM(port)

on=True
while (on):
    print('Functionality: \n \"raw serial\" | Prints Raw Serial Output \n \"change HV\" [value (V)] | changes the High Voltage to value given\n \"count rate" [time (s)] | measure the count rate over given time in seconds' )
    
    mode = input('Mode: ')

    if mode == ('raw serial'):
        ss.rawSerial()
    elif mode.contains('change HV'):
        ss.changeHV()
    elif mode.contains('count rate'):
        ss.countRate()
