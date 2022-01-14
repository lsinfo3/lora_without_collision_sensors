#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 14:03:14 2021

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
import random


#sim input
number_sensors = 765
sim_repetitions = 200

#sf distribution
sf_distribution = 'random' #possible: 'random', 'distance', todo: exponential; more likely?
#input for distance calc based on hata model

#payload distribution
payload_distribution = 'random' #todo exponential more likely?
payload_min = 1
payload_max = 51 #todo others - 50 since max for ToA?


number_accuracy = 6 #number of after comma positions

#channel access
channel_access = 'slotted' #possible: aloha; slotted; lbt; other (any other or selective strategy)
number_channels = 1

channel_selection = 'random' #tbt - other?


#lora related parameters
payload_bytes = 1
cyclic_redundancy_check = 1
header_enabled = 1
header_length = 20
low_datarate_optimize = 0
coding_rate = 4
preamble_length = 8
bandwidth = 125000
  

slot_length = 4.705
slotted_guard_time=0#ms
drift_variation = np.linspace(0,0.1,1000)
ppm_drift = np.linspace(2,100,1000)
drift_per_second = np.linspace(0.0072,0.36,1000)/3600 #0.36: 100ppm per hour
slotted_max_time_drift = 0.36 #360ms as max time drift
sync_length = 8 #B
sf = [7,8,9,10,11,12]

sync_packet = (8 * sync_length - (4*np.array(sf)) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * np.array(sf) - 2*low_datarate_optimize)
n_sync_packet = 8 + (np.ceil(sync_packet)* (coding_rate + 4))
total_sync_symbols = preamble_length + 4.25 + n_sync_packet
symbol_duration = (2**np.array(sf))/bandwidth
sync_toa = symbol_duration * total_sync_symbols

j=0

total_drift = np.zeros((len(drift_per_second),sim_repetitions))
all_drifts = np.zeros((number_sensors, len(drift_per_second),sim_repetitions))
synchronizations = np.zeros((len(drift_per_second),sim_repetitions))


def slotted_aloha(dataframe, sensors, threshold):
    #collision check
 
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
    k = 0
    numbersyncs = 0
    for k in range(0,sensors-1):
        #check if drift exceeds limit   
        if dataframe['transmission_starts'][k+1] < dataframe['transmission_ends'][k]:
            dataframe['collisions'][k] = 1
            dataframe['collisions'][k + 1] = 1
            
        if dataframe['current_time_drift'][k] > threshold:
            #todo sync lost
            dataframe['transmission_starts'][k] = dataframe['transmission_starts'][k] - dataframe['current_time_drift'][k]
            dataframe['last_sync_time'][k]  = dataframe['transmission_ends'][k] 
            dataframe['transmission_ends'][k] = dataframe['transmission_ends'][k] - dataframe['current_time_drift'][k]
            dataframe['current_time_drift'][k] = 0
            numbersyncs = numbersyncs + 1
            
                
    if dataframe['current_time_drift'][k+1] > threshold:
            #todo sync lost
            dataframe['transmission_starts'][k+1] = dataframe['transmission_starts'][k+1] - dataframe['current_time_drift'][k+1]
            dataframe['last_sync_time'][k+1]  = dataframe['transmission_ends'][k+1] 
            dataframe['transmission_ends'][k+1] = dataframe['transmission_ends'][k+1] - dataframe['current_time_drift'][k+1]

            dataframe['current_time_drift'][k+1] = 0
            numbersyncs = numbersyncs + 1
            
                
    dataframe = dataframe.sort_values('index',ignore_index=True)
    return [numbersyncs, dataframe]
  
#last sync - letztes mal simuliert, current time - momentane startzeit, behavior 80/60/10 ppm, random drift vs. immer gleicher
#drift (drift up to 20ppm, schwankung um den "m"-Wert)
def calculate_clock_drift(dataframe, drift):
    #t = 5.4
    error_direction = np.random.randint(2, size=number_sensors)
    error_direction[np.where(error_direction == 0)] = -1
    difference = dataframe['transmission_starts'] - dataframe['last_sync_time']
    
    drift_error_index = np.random.randint(1000, size=number_sensors) 
    
    #next_drift_tmp = (dataframe['driftbehavior'] * difference * 1000 + t)/1000
    next_drift_tmp = drift * difference

    next_drift_error = drift_variation[drift_error_index] * error_direction
    
    next_drift_tmp = next_drift_tmp + next_drift_tmp * next_drift_error
    
    drift_diff = next_drift_tmp - dataframe['current_time_drift'] 
    dataframe['current_time_drift'] =  next_drift_tmp
    total_drift = np.sum(next_drift_tmp)
    dataframe['transmission_starts'] = dataframe['transmission_starts'] + drift_diff
    dataframe['transmission_ends'] = dataframe['transmission_ends'] + drift_diff
    return [total_drift, dataframe]


for i in range(len(drift_per_second)):    
    #i = 990
    possible_slots = np.linspace(0,3600-slot_length,number_sensors)
        
    sensor_index = np.arange(number_sensors)+1
    
    sensor_dataframe = pd.DataFrame({'index': sensor_index})
    sensor_dataframe['transmission_attempts'] = np.ones(number_sensors)
    
    spreading_factor = np.random.randint(6,size=number_sensors)+7
    sensor_dataframe['spreading_factor'] = spreading_factor
    
    payload = np.random.randint(payload_max,size=number_sensors)+payload_min
    sensor_dataframe['payload'] = payload
        
    #time on air calculation
    all_packet = (8 * sensor_dataframe['payload'] - (4*sensor_dataframe['spreading_factor']) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * sensor_dataframe['spreading_factor'] - 2*low_datarate_optimize)
    n_packet = 8 + (np.ceil(all_packet)* (coding_rate + 4))
    total_symbols = preamble_length + 4.25 + n_packet
    symbol_duration = (2**sensor_dataframe['spreading_factor'])/bandwidth
    sensor_dataframe['time_on_air'] = symbol_duration * total_symbols
    
    
    sensor_dataframe['transmission_starts'] = possible_slots[random.sample(range(0, len(possible_slots)), number_sensors)] 
    sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_starts'] + sensor_dataframe['time_on_air']
    sensor_dataframe['current_time_drift'] = np.zeros(number_sensors)
    sensor_dataframe['last_sync_time'] = np.zeros(number_sensors)
    tmp_timedrifts = np.zeros(number_sensors)
    
    #tmp_driftbehavior = np.random.randint(10, size=number_sensors) + 1
    #tmp_timedrifts[np.where(tmp_driftbehavior > 0)] = 0.00006119496855
    #tmp_timedrifts[np.where(tmp_driftbehavior > 0)] = 0.000081083333 #== 1
    #tmp_timedrifts[np.where(tmp_driftbehavior > 0)] = 0.00002047558923
    #sensor_dataframe['driftbehavior'] = tmp_timedrifts
    
    
    sensor_dataframe['message_type'] = np.zeros(number_sensors) #0: sensor message, 1: gw message

    for j in range(sim_repetitions):
        print("i = " + str(i))
        print("j = " + str(j))
        [total_drift[i][j], sensor_dataframe] = calculate_clock_drift(sensor_dataframe, drift_per_second[i])
        all_drifts[:,i,j] = sensor_dataframe['current_time_drift']
        [synchronizations[i][j], sensor_dataframe] = slotted_aloha(sensor_dataframe, number_sensors, slotted_max_time_drift) #full dataframe to function if all sensors use aloha
        sensor_dataframe['transmission_starts'] = sensor_dataframe['transmission_starts'] + 3600
        sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_ends'] + 3600
        
#%% 
columnsarray = []
for i in range(200):
    columnsarray.append(str(i))
    
    
syn_dataframe = pd.DataFrame(synchronizations, columns=columnsarray)
syn_dataframe['resyn_drift'] = drift_per_second

syn_dataframe.to_csv('syn_dataframe_diff_drifts.csv') 

#%%
total_drift_dataframe = pd.DataFrame(total_drift, columns=columnsarray)
syn_dataframe['resyn_drift'] = drift_per_second

total_drift_dataframe.to_csv('total_drift_dataframe_diff_drifts.csv') 

#%%
#if only plot required, load syn dataframe; last column is drift per second information
#found in "slotted time drift study" in results folder
import matplotlib.pyplot as plt
theory_array = np.zeros(1000)
p_sync_theory = np.zeros(1000)
p_sync_theory_lower = np.zeros(1000)
theory_array[0] = 0.36
for l in range(len(theory_array)):
    if l > 0:
        theory_array[l] = 0.36/(l)
    p_sync_theory[l] = 1/(l+1)
    p_sync_theory_lower[l] = 1/(l+2)
    

theory_array_modified = theory_array + theory_array*0.1
theory_array_modified_minus = theory_array - theory_array*0.1
#threshold_theory = 
n = 5
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1, figsize=(5, 3))


plt.plot(drift_per_second*3600,np.mean(synchronizations, axis=1)/number_sensors, color=colors[0], linewidth = 2, label='simulation')
plt.step(np.flip(theory_array), np.flip(p_sync_theory), drawstyle='steps-post', color=colors[3], linewidth = 2, label='model')
plt.step(np.flip(theory_array_modified), np.flip(p_sync_theory), color=colors[2], linewidth = 1.3, linestyle='dashed', label='model 'u"\u00B1"'10%')
plt.step(np.flip(theory_array_modified_minus), np.flip(p_sync_theory), color=colors[2], linestyle='dashed', linewidth = 1)

#plt.step(np.flip(p_sync_theory_lower), np.flip(p_sync_theory))

plt.ylabel('P(sync)')
plt.xlabel('drift per hour [s]')
plt.xlim(0,0.25)
plt.ylim(0,0.6)
plt.grid(which='major')
tmp = plt.legend(loc="best", labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.gcf().subplots_adjust(bottom=0.18)
plt.gcf().subplots_adjust(left=0.13)
plt.savefig('../figures/time_drift_analysis.pdf')
