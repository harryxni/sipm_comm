#!/usr/bin/env python3
import serial
import sys


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
    def rawSerial(self,value):
        return((self.sr.readline())
    def countRate(self,time):
        pass


