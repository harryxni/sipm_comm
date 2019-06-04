#!/usr/bin/env python3
import serial
import io
from pyfiglet import Figlet
import sys
f=Figlet(font='univers')
print(f.renderText('ArduSiPM'))
import serialScripts as ss
import csv
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
    sipm1=ss.ArduSiPM(port1)
    sipm2=ss.ArduSiPM(port2)

on=True
while (on):
    print('Functionality: \n \"rawserial\" | Prints Raw Serial Output \n \"changeV\" [value (V)] | changes the High Voltage to value given\n \"countrate" [time (s)] | measure the count rate over given time in seconds \n \"CoincidentCount" [time (s)] | Count coincident triggers for time given in seconds \n \"exit" |Closes Program' )
    
    mode = input('Mode: ')
    args = mode.split(' ')

    if args[0] == ('rawserial'):
        while 1==1:
            print(sipm1.rawSerial())
    elif args[0] == 'changeV':
        v_value = float(args[1])
        sipm1.changeV(v_value)
    elif args[0]== 'countrate':
        time_amt=int(args[1])
        print('Taking Data for ' + str(time_amt) + ' seconds' )
        rate, rate_err, adcs, tdcs=sipm1.countRate(time_amt)

        print('Count Rate #/s: ' + str(rate) + '+\-' + str(rate_err))
        save_vals=input('Save Data[y/n]: ')
        if save_vals=='y':
            filename=input('Filename: ' )
            with open(filename, 'w') as f:
                hv, thr, sr = sipm1.getInfo()
                f.write('Count Rate:' + str(rate) + '\n')
                f.write('Run Time (s): ' + str(time_amt) + '\n')
                f.write(hv + '\n')
                f.write(thr + '\n')
                f.write(sr + '\n')

                writer=csv.writer(f, delimiter='\t')
                writer.writerows(zip(tdcs,adcs))


    elif args[0]=='liveplot':
        time_amt=int(args[1])
        sipm1.liveplot(time_amt)

    elif args[0]=='CoincidentCount':
        time_amt=int(args[1])
        cc=ss.Coincidence(sipm1,sipm2)
        cc.countCoincidences(time_amt)
    elif args[0]=='getinfo':
        sipm1.getInfo()

    elif args[0]=='exit':
        break

