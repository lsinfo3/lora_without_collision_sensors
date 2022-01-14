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

base_filename=r"SF"
SF=[12]
configs=["pure","slotted"]
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

plt.rcParams.update({'font.size': 26})
colors = plt.cm.copper(np.linspace(0,1,len(SF)))
plt.figure(1, figsize=(12, 6))
for sf in SF:
    plt.rcParams.update({'font.size': 26})
    plt.figure(1, figsize=(10, 6))
    x=[]
    y=[]
    for i in range(0,len(configs)):
        x=[]
        y=[]
        with open(base_filename+str(sf)+str(configs[i])+".csv", newline='') as csvfile:
            data = list(csv.reader(csvfile))
            for curr in range(1,len(data)):
                x.append(int(data[curr][1]))
                y.append(float(data[curr][2]))
        if(i==1):
            plt.plot(x,y, color=colors[SF.index(sf)],label="SF"+str(sf),linewidth=3.0)
        else:
            plt.plot(x,y,linestyle=(0, (5, 10)), color=colors[SF.index(sf)],linewidth=3.0)
plt.xlabel('number of sensors')
plt.ylabel('collision probability %')
plt.xscale('log')
plt.grid(which='major')
plt.legend(loc="best",bbox_to_anchor=(1.05, 1))#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
plt.gcf().subplots_adjust(bottom=0.19)
plt.gcf().subplots_adjust(right=0.7)
plt.gcf().subplots_adjust(left=0.18)
plt.savefig('SF'+str(sf)+'Allinone.pdf')
plt.show()
plt.close()
            
