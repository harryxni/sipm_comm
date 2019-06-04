#!/usr/bin/env python3
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

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
        self.sr.write(value.encode())
    
    def getInfo(self):
        self.sr.reset_input_buffer()
        self.serWrite('m')
        time.sleep(1)
        menulines=''
        while self.sr.inWaiting()>0:
            menulines+= (self.sr.readline()).decode('UTF-8')
        
        self.serWrite('e')
        lines=menulines.splitlines()
        hv_string=[x for x in lines if 'HVCODE' in x and '=' in x][0]
        thr_string=[x for x in lines if 'Threshold (mv)' in x and '=' in x][0]
        rate_string=[x for x in lines if 'Sample rate' in x and '=' in x][0]
        print(hv_string)
        print(thr_string)
        print(rate_string)

        return hv_string, thr_string, rate_string 



    def changeV(self,hv):
        dac_code=int(1.5 + (71.8 - hv)/0.1786)
        self.serWrite('%' + str(dac_code))
        self.sr.reset_input_buffer()
        return(dac_code)
    
    def changeThres(self, value):
        pass
    
    def changeSampleT(self, value):
        pass
    
    def rawSerial(self):
        return(str(self.sr.readline()))

    def lineRead(self,line_in):
        #line_in is a line which includes ADC and TDC data from serial
        loc=line_in.index('v')
        endloc=line_in.index('$')
        num=int(line_in[endloc+1]) 
        tloc=line_in.index('t')
        if num==1:
            adc=line_in[loc+1:endloc] 
            tdc=line_in[tloc+1: loc]
            #print(adc)
            #print(tdc)
        elif num>1:
            adc=[]
            tdc=[]
            substrings=line_in[tloc+1:endloc].split('t')
            for val in substrings:
                adc.append(val.split('v')[1])
                tdc.append(val.split('v')[0])
        return (num, adc, tdc)
       
    def countRate(self,amt_time):
        #time in seconds
        
        self.serWrite('@')
        time.sleep(0.5)
        self.sr.reset_input_buffer()
        
        stop_time=time.time() + amt_time
        num_muons=0
        adcs=[]
        tdcs=[]
        while time.time()<stop_time:
            line=self.rawSerial()
            count_loc=line.index('$')

            print(line)
            if 'v' in line and line[count_loc+1]!='0':
                count, adc_val, tdc_val=self.lineRead(line)
                num_muons+=count
                if count==1:
                    adcs.extend([adc_val])
                    tdcs.extend([tdc_val])
                elif count>1:
                    for val in adc_val:
                        adcs.append(val)
                    for val in tdc_val:
                        tdcs.append(val)

                print(num_muons)
            rate=num_muons/amt_time
            error=np.sqrt(num_muons)/amt_time 
        print(adcs)
        print(tdcs)
        dec_adcs=[int(x,16) for x in adcs]
        dec_tdcs=[int(x,16) for x in tdcs]

        plt.hist(dec_adcs)
        plt.show()
        return rate, error, dec_adcs, dec_tdcs
    
    def animate(self, amt_time): 
        self.serWrite('@')
        time.sleep(0.5)
        self.sr.reset_input_buffer()
        
        stop_time=time.time() + amt_time
        num_muons=0
        while time.time()<stop_time:
            line=self.rawSerial()
            adcs=[]
            tdcs=[]
            print(line)
            if 'v' in line and 'Threshold' not in line:
                count, adc_val, tdc_val=self.lineRead(line)
                num_muons+=count
                adcs.append(int(adc_val,16))
                tdcs.append(int(tdc_val,16))
            self.ax1.clear()
            self.ax1.hist(adcs)
    def liveplot(self, amt_time):
        self.fig=plt.figure()
        self.ax1=self.fig.add_subplot(1,1,1)
        ani=anim.FuncAnimation(self.fig,self.animate, interval=1000)
        plt.show()
                    

class Coincidence:
    def __init__(self, pm1, pm2):
         self.prim=pm1
         self.rep=pm2
    def countCoincidences(self, amt_time):
        self.prim.serWrite('@')
        self.rep.serWrite('@')
        time.sleep(0.5)
        self.rep.serWrite('/2')
        time.sleep(0.5)
        self.prim.sr.reset_input_buffer()
        self.rep.sr.reset_input_buffer()
        num_coin=0
        
        stop_time=time.time() + amt_time

        while time.time()<stop_time:
            prim_line=self.prim.rawSerial()
            rep_line=self.rep.rawSerial()
            print(prim_line, rep_line)
            if 'v' in prim_line and 'v' in rep_line:
                p_results=self.prim.lineRead(prim_line)
                r_results=self.rep.lineRead(rep_line)
                num_coin+=int(p_results[0])

                print('Coincidence Detected within One Second')
               if p_results[0] != 1 or r_results[0] !=1:
                    min_num=(p_results[0], r_results[0])
                    min_results=[x for x in [p_results, r_results] if x[0]==min_num]
                    print(min_results)
                else:
                     p_tdc=int(p_results[2],16)
                    r_tdc=int(r_results[2],16)
                
                    print('Difference of' + str(np.abs(p_tdc-r_tdc)) + ' microseconds')

                #if p_results[0]==1:
                #    if p_results[2]==r_results[2]:
                #        print('Microsecond Coincidence')
