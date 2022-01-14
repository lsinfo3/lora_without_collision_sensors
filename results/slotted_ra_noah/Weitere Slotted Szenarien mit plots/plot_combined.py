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

#scenarios=["binary_sensors","small_nodes","small_nodes_sf12","weather_station","weather_station_sf12"]
scenarios=["binary sensors", "small nodes", "small nodes SF12", "weather station", "weather station SF12"]
toa=[207,42,1155,616,2301]
percentages=[1,2,5,10]


plt.rcParams.update({'font.size': 22})
colors = plt.cm.copper(np.linspace(0,1,len(scenarios)))
plt.figure(1, figsize=(10, 6))
x=[]
y=[]    
for percent in percentages:
    plt.rcParams.update({'font.size': 22})
    colors = plt.cm.copper(np.linspace(0,1,len(scenarios)))
    plt.figure(1, figsize=(10, 6))
    xp=[]
    yp=[]
    for i in range(0,len(scenarios)):
        hit=False
        with open(str(scenarios[i])+".csv", newline='') as csvfile:
            data = list(csv.reader(csvfile))
            for curr in range(1,len(data)):
                if(float(data[curr][2])>=(percent/100) and not hit):
                    hit=True
                    xp.append(toa[i])
                    yp.append(curr*10)
    plt.plot(xp,yp,'o', color=colors[0])
    #try:
    #    z = np.polyfit(xp, yp, 1)
    #    p = np.poly1d(z)
    #    plt.plot(xp,p(xp),"r--")
    #    # the line equation:
    #    print("y=%.6fx+(%.6f)"%(z[0],z[1]))
    #    plt.plot(xp,yp,'o', color=colors[0],label="y=%.6fx+(%.6f)"%(z[0],z[1]))
    #except:
    #    pass
    plt.xlabel('ToA [ms]')
    plt.ylabel('device with '+str(percent)+'% collision probability')
    #plt.xscale('log')
    plt.grid(which='major')
    #plt.legend(loc="best")#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
    plt.gcf().subplots_adjust(bottom=0.19)
    plt.gcf().subplots_adjust(left=0.18)
    plt.savefig(str(percent)+'all_percentage.pdf')
    #plt.show()
    plt.close()
