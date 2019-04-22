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
elif len(sys.argv)==2:
    port1=sys.argv[1]
    sipm1=ss.ArduSiPM(port1)
elif len(sys.argv)==3:
    port1=sys.argv[1]
    port2=sys.argv[2]
    sipm2=ss.ArduSiPM(port2)

on=True
while (on):
    print('Functionality: \n \"raw serial\" | Prints Raw Serial Output \n \"change HV\" [value (V)] | changes the High Voltage to value given\n \"count rate" [time (s)] | measure the count rate over given time in seconds' )
    
    mode = input('Mode: ')

    if mode == ('raw serial'):
        on=True
        while on:
            print(sipm1.rawSerial())

    elif 'change HV' in mode:
        sipm1.changeHV()
    elif 'count rate' in mode:
        time_amt=[int(s) for s in mode.split(' ') if s.isdigit()]
        print(time_amt)
        sipm1.countRate(time_amt[0])
