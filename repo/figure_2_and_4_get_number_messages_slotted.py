#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 09:23:12 2021

@author: frank
"""

try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#lora related parameters
payload_bytes = 1
cyclic_redundancy_check = 1
header_enabled = 1
header_length = 20
low_datarate_optimize = 0
coding_rate = 4
preamble_length = 8
bandwidth = 125000
  
sync_length = 6 #B
sf = [7,8,9,10,11,12]
drift_per_hour = np.linspace(0.0036,7.20,2000)
randomness = 0.1

sync_packet = (8 * sync_length - (4*np.array(sf)) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * np.array(sf) - 2*low_datarate_optimize)
n_sync_packet = 8 + (np.ceil(sync_packet)* (coding_rate + 4))
total_sync_symbols = preamble_length + 4.25 + n_sync_packet
symbol_duration = (2**np.array(sf))/bandwidth
sync_toa = symbol_duration * total_sync_symbols

duty_cycle = 0.01

number_sensors = np.arange(2000)+1
max_packet_toa = 3.023

p_sync_7 = (0.01*3600)/(number_sensors * sync_toa[0])
p_sync_8 = (0.01*3600)/(number_sensors * sync_toa[1])
p_sync_9 = (0.01*3600)/(number_sensors * sync_toa[2])
p_sync_10 = (0.01*3600)/(number_sensors * sync_toa[3])
p_sync_11 = (0.01*3600)/(number_sensors * sync_toa[4])
p_sync_12 = (0.01*3600)/(number_sensors * sync_toa[5])



k_7 = 1/p_sync_7
k_8 = 1/p_sync_8
k_9 = 1/p_sync_9
k_10 = 1/p_sync_10
k_11 = 1/p_sync_11
k_12 = 1/p_sync_12

drift_limit7 = np.zeros(len(number_sensors))-1
drift_limit8 = np.zeros(len(number_sensors))-1
drift_limit9 = np.zeros(len(number_sensors))-1
drift_limit10 = np.zeros(len(number_sensors))-1
drift_limit11 = np.zeros(len(number_sensors))-1
drift_limit12 = np.zeros(len(number_sensors))-1

for i in range(len(drift_per_hour)):
    possible_sensors_7 = 3600/(k_7 * drift_per_hour[i] + drift_per_hour[i] + drift_per_hour[i]*randomness + sync_toa[0] + max_packet_toa)
    drift_limit7[np.where((possible_sensors_7 - number_sensors) > 0)] = number_sensors[i]
    possible_sensors_8 = 3600/(k_8 * drift_per_hour[i] + drift_per_hour[i] + drift_per_hour[i]*randomness + sync_toa[1] + max_packet_toa)
    drift_limit8[np.where((possible_sensors_8 - number_sensors) > 0)] = number_sensors[i]
    possible_sensors_9 = 3600/(k_9 * drift_per_hour[i] + drift_per_hour[i] + drift_per_hour[i]*randomness + sync_toa[2] + max_packet_toa)
    drift_limit9[np.where((possible_sensors_9 - number_sensors) > 0)] = number_sensors[i]
    possible_sensors_10 = 3600/(k_10 * drift_per_hour[i] + drift_per_hour[i] + drift_per_hour[i]*randomness + sync_toa[3] + max_packet_toa)
    drift_limit10[np.where((possible_sensors_10 - number_sensors) > 0)] = number_sensors[i]
    possible_sensors_11 = 3600/(k_11 * drift_per_hour[i] + drift_per_hour[i] + drift_per_hour[i]*randomness + sync_toa[4] + max_packet_toa)
    drift_limit11[np.where((possible_sensors_11 - number_sensors) > 0)] = number_sensors[i]
    possible_sensors_12 = 3600/(k_12 * drift_per_hour[i] + drift_per_hour[i] + drift_per_hour[i]*randomness + sync_toa[5] + max_packet_toa)
    drift_limit12[np.where((possible_sensors_12 - number_sensors)> 0)] = number_sensors[i]


#%%
#max messages per hour
drift_threshold = np.linspace(0.0001, 10, 10000)

max_messages_per_hour = 3600/(sync_toa[5] + max_packet_toa + 2 * drift_threshold)

max_messages_per_hour_100ppm = (((drift_threshold/0.36) - 1) * 0.01 * 3600)/sync_toa[5]

max_messages_per_hour_2ppm = (((drift_threshold/0.0072) - 1) * 0.01 * 3600)/sync_toa[5]

max_messages_per_hour_20ppm = (((drift_threshold/0.072) - 1) * 0.01 * 3600)/sync_toa[5]


n = 4
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1, figsize=(5, 3))


plt.plot(max_messages_per_hour, drift_threshold, color=colors[0], linewidth = 2, label='limit messages \nper hour')
plt.plot(max_messages_per_hour_100ppm, drift_threshold, color=colors[1], linewidth = 2, label='limit 100ppm')
plt.plot(max_messages_per_hour_20ppm, drift_threshold, color=colors[2], linewidth = 2, label='limit 20ppm')
plt.plot(max_messages_per_hour_2ppm, drift_threshold, color=colors[3], linewidth = 2, label='limit 2ppm')


plt.ylabel('drift threshold [s]')
plt.xlabel('max messages per hour')
plt.xlim(0,1000)
plt.ylim(0,4)
#plt.ylim(0,0.6)
plt.grid(which='major')
tmp = plt.legend(loc="best", labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.gcf().subplots_adjust(bottom=0.18)
plt.gcf().subplots_adjust(left=0.13)
plt.savefig('../figures/slotted_max_messages_per_hour.pdf')
#%%
n = 6
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(2, figsize=(5, 3))


plt.plot(number_sensors, p_sync_7, color=colors[0], linewidth = 2, label='SF 7')
plt.plot(number_sensors, p_sync_8, color=colors[1], linewidth = 2, label='SF 8')
plt.plot(number_sensors, p_sync_9, color=colors[2], linewidth = 2, label='SF 9')
plt.plot(number_sensors, p_sync_10, color=colors[3], linewidth = 2, label='SF 10')
plt.plot(number_sensors, p_sync_11, color=colors[4], linewidth = 2, label='SF 11')
plt.plot(number_sensors, p_sync_12, color=colors[5], linewidth = 2, label='SF 12')

#plt.plot(max_messages_per_hour_100ppm, drift_threshold, color=colors[1], linewidth = 2, label='limit 100ppm')
#plt.plot(max_messages_per_hour_20ppm, drift_threshold, color=colors[2], linewidth = 2, label='limit 20ppm')
#plt.plot(max_messages_per_hour_2ppm, drift_threshold, color=colors[3], linewidth = 2, label='limit 2ppm')


plt.ylabel('tolerated P(sync)')
plt.xlabel('number messages per hour')
#plt.xlim(0,1000)
plt.ylim(0,1)
plt.grid(which='major')
tmp = plt.legend(loc="best", ncol = 2, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.gcf().subplots_adjust(bottom=0.18)
plt.gcf().subplots_adjust(left=0.18)
plt.savefig('../figures/p_sync_threshold.pdf')
#%%
n = 6
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(3, figsize=(5, 3))


plt.plot(number_sensors, drift_limit7, color=colors[0], linewidth = 2, label='SF 7')
plt.plot(number_sensors, drift_limit8, color=colors[1], linewidth = 2, label='SF 8')
plt.plot(number_sensors, drift_limit9, color=colors[2], linewidth = 2, label='SF 9')
plt.plot(number_sensors, drift_limit10, color=colors[3], linewidth = 2, label='SF 10')
plt.plot(number_sensors, drift_limit11, color=colors[4], linewidth = 2, label='SF 11')
plt.plot(number_sensors, drift_limit12, color=colors[5], linewidth = 2, label='SF 12')

#plt.plot(max_messages_per_hour_100ppm, drift_threshold, color=colors[1], linewidth = 2, label='limit 100ppm')
#plt.plot(max_messages_per_hour_20ppm, drift_threshold, color=colors[2], linewidth = 2, label='limit 20ppm')
#plt.plot(max_messages_per_hour_2ppm, drift_threshold, color=colors[3], linewidth = 2, label='limit 2ppm')


plt.ylabel('maximal clock drift [ppm]')
plt.xlabel('number messages per hour')
#plt.xlim(0,1000)
plt.ylim(0,200)
plt.grid(which='major')
tmp = plt.legend(loc="best", ncol = 2, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.gcf().subplots_adjust(bottom=0.18)
plt.gcf().subplots_adjust(left=0.18)
plt.savefig('../figures/drift_threshold_ppm.pdf')




