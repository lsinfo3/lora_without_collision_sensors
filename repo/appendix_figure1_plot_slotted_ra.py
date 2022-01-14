#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:35:37 2021

@author: frank
"""

try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import random
pd.options.mode.chained_assignment = None



random_sf_pure = pd.read_json('/home/frank/Documents/Papers/2021_usenix_slotted_lora/sensors/results/slotted_ra_noah/PureVSSlottedfeinereabstaende/SF12pure.json') 
random_sf_slotted = pd.read_json('/home/frank/Documents/Papers/2021_usenix_slotted_lora/sensors/results/slotted_ra_noah/PureVSSlottedfeinereabstaende/SF12slotted.json')  

random_sf_10_pl51_pure = pd.read_json('/home/frank/Documents/Papers/2021_usenix_slotted_lora/sensors/results/slotted_ra_noah/WeitereSzenarienSlottedundPureALOHA/SF10PL51Pure.json') 
random_sf_10_pl51 = pd.read_json('/home/frank/Documents/Papers/2021_usenix_slotted_lora/sensors/results/slotted_ra_noah/WeitereSzenarienSlottedundPureALOHA/SF10PL51.json') 

random_sf_12_pl10_pure = pd.read_json('/home/frank/Documents/Papers/2021_usenix_slotted_lora/sensors/results/slotted_ra_noah/WeitereSzenarienSlottedundPureALOHA/SF12PL10Pure.json') 
random_sf_12_pl10 = pd.read_json('/home/frank/Documents/Papers/2021_usenix_slotted_lora/sensors/results/slotted_ra_noah/WeitereSzenarienSlottedundPureALOHA/SF12PL10.json') 





random_sf_pure_collisions = random_sf_pure['collisions']
random_sf_slotted_collisions = random_sf_slotted['collisions']
collisions_RA_SF = np.zeros(len(random_sf_pure_collisions))
collisions_Slotted_SF = np.zeros(len(random_sf_pure_collisions))
for i in range(len(random_sf_pure_collisions)):
    collisions_RA_SF[i] = np.mean(random_sf_pure_collisions[i])
    collisions_Slotted_SF[i] = np.mean(random_sf_slotted_collisions[i])

collisions_RA_SF = np.delete(collisions_RA_SF,0)
collisions_Slotted_SF = np.delete(collisions_Slotted_SF,0)

n = 5
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1,figsize=(5, 3))
plt.plot(np.arange(1,2001), np.sort(collisions_RA_SF),color=colors[0], linewidth = 2, label='RA: R')
plt.plot(np.arange(1,2001), np.sort(collisions_Slotted_SF),color=colors[0], linestyle='dashed', linewidth = 2, label='Slotted: R') 

plt.plot(random_sf_10_pl51_pure['X'], np.sort(random_sf_10_pl51_pure['collisions']),color=colors[2], linewidth = 2, label='RA: SF10')
plt.plot(random_sf_10_pl51['X'], np.sort(random_sf_10_pl51['collisions']),color=colors[2], linestyle='dashed', linewidth = 2, label='Slotted: SF10')

plt.plot(random_sf_12_pl10_pure['X'], np.sort(random_sf_12_pl10_pure['collisions']),color=colors[4], linewidth = 2, label='RA: SF12')
plt.plot(random_sf_12_pl10['X'], np.sort(random_sf_12_pl10['collisions']),color=colors[4], linestyle='dashed', linewidth = 2, label='Slotted: SF12')
# =============================================================================
# plt.plot(number_sensors, all_collisions_10_ra,color=colors[1], linewidth = 2, label='10%')
# plt.plot(number_sensors, all_collisions_20_ra,color=colors[2], linewidth = 2, label='20%')
# plt.plot(number_sensors, all_collisions_50_ra,color=colors[3], linewidth = 2, label='50%')
# plt.plot(number_sensors, all_collisions_100_ra, color=colors[4], linewidth = 2, label='100%') 
# 
# plt.plot(number_sensors, all_collisions_0_ra_sf,color=colors[0], linestyle='dashed',linewidth = 2)
# plt.plot(number_sensors, all_collisions_10_ra_sf,color=colors[1], linestyle='dashed',linewidth = 2)
# plt.plot(number_sensors, all_collisions_20_ra_sf,color=colors[2], linestyle='dashed',linewidth = 2)
# plt.plot(number_sensors, all_collisions_50_ra_sf,color=colors[3], linestyle='dashed',linewidth = 2)
# plt.plot(number_sensors, all_collisions_100_ra_sf, color=colors[4],linestyle='dashed', linewidth = 2)  
# =============================================================================
plt.ylim(-0.02, 0.6)
plt.grid(which='major')
plt.legend(loc='best', ncol=1, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.xlabel('number messages per hour')
plt.ylabel('collision probability')
plt.gcf().subplots_adjust(bottom=0.18)
#plt.gcf().subplots_adjust(left=0.15)
plt.savefig('../figures/appendix_slotted_ra.pdf') 