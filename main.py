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
    sipm1=ss.ArduSiPM(port)
elif len(sys.argv)==2:
    port1=sys.argv[1]
    sipm1=ss.ArduSiPM(port1)
elif len(sys.argv)==3:
    port1=sys.argv[1]
    port2=sys.argv[2]
    sipm2=ss.ArduSiPM(port2)

on=True
while (on):
    print('Functionality: \n \"rawserial\" | Prints Raw Serial Output \n \"changeV\" [value (V)] | changes the High Voltage to value given\n \"countrate" [time (s)] | measure the count rate over given time in seconds' )
    
    mode = input('Mode: ')
    args = mode.split(' ')

    if args[0] == ('rawserial'):
        while 1==1:
            print(sipm1.rawSerial())
    elif args[0] == 'changeV':
        v_value = args[1]
        sipm1.changeHV()v_value
    elif args[0]== 'countrate':
        time_amt=int(args[1])
        print('Taking Data for ' + str(time_amt) + ' seconds' )
        rate=sipm1.countRate(time_amt)
        rate_err = np.sqrt(rate)/time_amt

        print('Count Rate #/s: ' + str(rate) + '+\-' + str(rate_err))

