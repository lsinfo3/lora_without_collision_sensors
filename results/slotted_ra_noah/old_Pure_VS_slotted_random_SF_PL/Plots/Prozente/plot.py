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
slot_lengths=[1,8,15,20,50,100,200]

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

plt.rcParams.update({'font.size': 14})
colors = plt.cm.copper(np.linspace(0,1,len(slot_lengths)+1))
plt.figure(1, figsize=(10, 6))


#x=[]
#y=[]
#with open(r"Sensors10000 SF7 PL8_BASELINE.csv", newline='') as csvfile:
#    data = list(csv.reader(csvfile))
#    for curr in range(1,len(data)):
#        x.append(int(data[curr][1]))
#        y.append(float(data[curr][2]))
#plt.plot(x,y, color=colors[0], label='SL+GT: 36ms')

for sf in SF:
    x=[]
    y=[]
    with open(r"Sensors10000 SF"+str(sf)+" PL8 SL8 GT1.csv", newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for curr in range(1,len(data)):
            x.append(int(data[curr][1]))
            y.append(float(data[curr][2]))
    plt.plot(x,y, color=colors[0], label='SL+GT: '+str(int(payload_size_to_time(8,sf)))+'ms')
    variable_end=[]
    variable_end_title=[]
    for sl in slot_lengths:
        variable_end.append(int(payload_size_to_time(sl,sf)))
        variable_end_title.append(round(1.25*payload_size_to_time(sl,sf),1))
    print(variable_end_title)
    for i in range(0,len(variable_end)):
        x=[]
        y=[]
        with open(base_filename+str(sf)+" PL8 SL"+str(variable_end[i])+".csv", newline='') as csvfile:
            data = list(csv.reader(csvfile))
            for curr in range(1,len(data)):
                x.append(int(data[curr][1]))
                y.append(float(data[curr][2]))
        plt.plot(x,y, color=colors[i+1], label='SL+GT: '+str(variable_end_title[i])+'ms')

    plt.xlabel('Number of Sensors')
    plt.ylabel('Collision probability % ToA: '+str(int(payload_size_to_time(8,sf)))+'ms')
    plt.xscale('log')
    plt.grid(which='major')
    plt.legend(loc="best")#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
    plt.gcf().subplots_adjust(bottom=0.19)
    plt.gcf().subplots_adjust(left=0.18)
    #plt.savefig(r'D:\DATA\Dokumente\Studium\Semester_6\Bachelorarbeit\4Sim\2021_06_02_Szenario_1\Plots\Roh\SF'+str(sf)+'.pdf')
    plt.show()
    plt.close()