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

for scenario in scenarios:
    plt.rcParams.update({'font.size': 22})
    colors = plt.cm.copper(np.linspace(0,1,len(scenarios)))
    plt.figure(1, figsize=(10, 6))
    x=[]
    y=[]
    with open(str(scenario)+".csv", newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for curr in range(1,len(data)):
            x.append(int(data[curr][1]))
            y.append(float(data[curr][2]))
    plt.plot(x,y, color=colors[scenarios.index(scenario)],label=scenario)
plt.xlabel('Number of Sensors')
plt.ylabel('Collision probability %')
plt.xscale('log')
plt.grid(which='major')
plt.legend(loc="best")#, handleheight=0.9, labelspacing=0.2, handlelength=0.7,fontsize=13)#,
plt.gcf().subplots_adjust(bottom=0.19)
plt.gcf().subplots_adjust(left=0.18)
plt.savefig('all.pdf')
#plt.show()
plt.close()          
