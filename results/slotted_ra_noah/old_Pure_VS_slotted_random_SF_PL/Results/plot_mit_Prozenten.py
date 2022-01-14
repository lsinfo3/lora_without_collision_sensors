import matplotlib.pyplot as plt
import numpy as np
import csv
import json
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
names=["pure ALOHA","slotted ALOHA"]
percentages=[1,2,5,10,15,20,25]

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
    colors = plt.cm.copper(np.linspace(0,1,len(configs)))
    plt.figure(1, figsize=(10, 6))
    x=[]
    y=[]
    for i in range(0,len(configs)):
        x=[]
        y=[]
        with open(base_filename+str(sf)+str(configs[i])+".json", newline='') as csvfile:
            data = json.load(csvfile)
            for curr in range(1,len(data['X'])):
                x.append(int(data['X'][str(curr)]))
                ytemp=0
                for run in range(1,10):
                    ytemp+=float(data['collisions'][str(curr)][run])
                y.append(ytemp/10)
        plt.plot(x,y, color=colors[i], label=str(names[i]))
    plt.xlabel('Number of Sensors')
    plt.ylabel('Collision probability % ToA: '+'ms')
    plt.xscale('log')
    plt.grid(which='major')
    plt.legend(loc="best")#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
    plt.gcf().subplots_adjust(bottom=0.19)
    plt.gcf().subplots_adjust(left=0.18)
    plt.savefig('PL'+'SF'+str(sf)+'.pdf')
    #plt.show()
    plt.close()
    plt.rcParams.update({'font.size': 22})
    colors = plt.cm.copper(np.linspace(0,1,len(configs)))
    plt.figure(1, figsize=(10, 6))
    for percent in percentages:
        plt.rcParams.update({'font.size': 26})
        colors = plt.cm.copper(np.linspace(0,1,len(configs)))
        plt.figure(1, figsize=(10, 6))
        xp=[]
        yp=[]
        for i in range(0,len(configs)):
            xp.append(i)
            with open(base_filename+str(sf)+str(configs[i])+".json", newline='') as csvfile:
                data = json.load(csvfile)
                ytemp=[]
                for run in range(0,10):
                    hit=False
                    for curr in range(1,len(data['X'])):
                        if(float(data['collisions'][str(curr)][run])>=(percent/100) and not hit):
                            ytemp.append(curr*10)
                            hit=True
                yp.append(ytemp)
        
        print([xp,yp])
        plt.boxplot(yp,positions=xp,widths=[0.1 for i in range(0,len(xp))])
        plt.ylabel('number of devices before\n'+str(percent)+'% collision probability')
        plt.xticks([0,1],["pure ALOHA", "slotted ALOHA"])
        #plt.xscale('log')
        plt.grid(which='major')
        #plt.legend(loc="best")#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
        plt.gcf().subplots_adjust(bottom=0.19)
        plt.gcf().subplots_adjust(left=0.19)
        plt.savefig('SF'+str(sf)+'Percentage'+str(percent)+'.pdf')
        #plt.show()
        plt.close()
            
