#!/usr/bin/env python3
import serial
import sys
import time

class ArduSiPM:
    def __init__(self, in_port):
        port=in_port
        self.sr=None
        while(self.sr is None):
            try:
                self.sr=serial.Serial(port, 115200)
            except:
                print('Device not found.')
                port=input('Please Enter the Port: ')
                self.sr=None

    def changeHV(self,value):
        pass
    def rawSerial(self):
        return(str(self.sr.readline()))
    def countRate(self,amt_time):
        #time in seconds
        stop_time=time.time() + amt_time
        while time.time()<stop_time:
            line=self.rawSerial()
            if 'v' in line:
                print('Muon')
        
        
        pass


