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

    def serWrite(self, value):
        time.sleep(0.5)
        self.sr.write(value.encode())
    def changeV(self,hv):
        dac_code=int(1.5 + (71.8 - hv)/0.1786)
    
        self.sr.serWrite('m')
        self.sr.reset_input_buffer()
        self.sr.serWrite('h')
        self.sr.serWrite(dac_code)
        time.sleep(1)
        self.sr.reset_input_buffer()
        return(dac_code)
    def changeThres(self, value):
        pass
    def changeSampleT(self, value):
        pass
    def rawSerial(self):
        return(str(self.sr.readline()))
    def countRate(self,amt_time):
        #time in seconds
        
        self.serWrite('m')
        self.sr.reset_input_buffer()
        #[print(self.sr.readline()) for _ in range(14)]
        checkline=str(self.sr.readline())
        if 'ENABLE' in checkline:
            self.serWrite('a')
        self.serWrite('e')
        time.sleep(0.5)
        self.sr.reset_input_buffer()
        #print('aaa')
        stop_time=time.time() + amt_time
        num_muons=0
        while time.time()<stop_time:
            line=self.rawSerial()
            if 'v' in line and 'Threshold' not in line:
                print('Muon Detected')
                loc=line.index('$')
                num_muons+=int(line[loc+1]) 
                print(num_muons)
            rate=num_muons/amt_time
        return(rate)
