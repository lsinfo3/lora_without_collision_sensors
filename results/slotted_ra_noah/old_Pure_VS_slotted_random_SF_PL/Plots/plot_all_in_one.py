import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import pandas as pd
import sys
import random
import math
import matplotlib.pyplot as plt
from datetime import datetime
from multiprocessing import Pool
import time

base_filename=r"Sensors10000 SF"
SF=[7,8,9,10,11,12]
slot_lengths=[8]
guard_times=[1,2,5,7,9,10,12,15,17,20,25,30]
percentages=[5]

def payload_size_to_time(payload, sf):
    # data_rate_optimisation: BW 125kHz, SF>=11
    BW = 125
    PL = payload+3
    CR = 1
    CRC = 1
    H = 1
    DE = 0
    SF = sf
    npreamble = 8
    if(sf >= 11):
        DE = 1

    Rs = BW/(math.pow(2, SF))
    Ts = 1/(Rs)
    symbol = 8+max(math.ceil((8.0*PL-4.0*SF+28+16*CRC-20.0*H) /
                             (4.0*(SF-2.0*DE)))*(CR+4), 0)
    Tpreamble = (npreamble+4.25)*Ts
    Tpayload = symbol*Ts
    ToA = Tpreamble+Tpayload
    return ToA

for sf in SF:
    plt.rcParams.update({'font.size': 22})
    colors = plt.cm.copper(np.linspace(0,1,len(SF)))
    plt.figure(1, figsize=(10, 6))
    x=[]
    y=[]
    variable_end=[]
    variable_end_title=[]
    for sl in guard_times:
        variable_end.append((sl/100)*payload_size_to_time(8,sf))
        variable_end_title.append(round(1*payload_size_to_time(sl,sf),1))
    print(sf)
    for i in range(0,len(variable_end)):
        x=[]
        y=[]
        with open(base_filename+str(sf)+" PL8 SL"+str(int(payload_size_to_time(8,sf)))+" GT"+str(variable_end[i])+".csv", newline='') as csvfile:
            data = list(csv.reader(csvfile))
            for curr in range(1,len(data)):
                x.append(int(data[curr][1]))
                y.append(float(data[curr][2]))

    for percent in percentages:
        xp=[]
        yp=[]
        for i in range(0,len(variable_end)):
            hit=False
            with open(base_filename+str(sf)+" PL8 SL"+str(int(payload_size_to_time(8,sf)))+" GT"+str(variable_end[i])+".csv", newline='') as csvfile:
                data = list(csv.reader(csvfile))
                for curr in range(1,len(data)):
                    if(float(data[curr][2])>=(percent/100) and not hit):
                        hit=True
                        xp.append(guard_times[i])
                        yp.append(curr*10)
        try:
            z = np.polyfit(xp, yp, 1)
            p = np.poly1d(z)
            plt.plot(xp,p(xp),"r--")
            # the line equation:
            print("y=%.6fx+(%.6f)"%(z[0],z[1]))
            plt.plot(xp,yp,'o', color=colors[SF.index(sf)],label="SF"+str(sf)+" y=%.1fx+(%.1f)"%(z[0],z[1]))
        except:
            pass
plt.xlabel('guard time %')
plt.ylabel('device with '+str(percent)+'% collision probability')
#plt.xscale('log')
plt.grid(which='major')
#plt.legend(loc="best")#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
plt.gcf().subplots_adjust(bottom=0.19)
plt.gcf().subplots_adjust(left=0.18)
plt.savefig('SF'+str(sf)+'Percentage'+str(percent)+'.pdf')
#plt.show()
plt.close()
            
