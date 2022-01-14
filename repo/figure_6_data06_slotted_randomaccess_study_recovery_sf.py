#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 17:16:07 2021

@author: frank
"""

try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

#slotted ppm definitions
#150ppm: 370, k=9.54
#125ppm: 396, k=10.2
#100ppm: 430, k=11.1
#75ppm: 475, k=12.2
#50ppm: 540, k=13.9
#25ppm: 647, k=16.7
#20ppm: 679, k=17.5
#15ppm: 718, k=18.5
#10ppm: 765, k=19.7
#5ppm: 826, k=21.3
#2ppm: 873, k=22.5

import pandas as pd
import numpy as np
import random
import math

pd.options.mode.chained_assignment = None

#sim input
sim_repetitions = 200
number_drift_reconfigs = 10
#number sensors and resulting k-values to not exceed duty cycle - see formula in paper
number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
k_value = [23,22,20,19,18,17,14,13,12,11,10]
k_exact = [22.5,21.3,19.7,18.5,17.5,16.7,13.9,12.2,11.1,10.2,9.54]

#get possible percent cross traffic added as random access
percent_crosstraffic = [1,2,3,4,5,10,15,20,25,30,50]

payload_min = 1
payload_max = 51 #todo others - 50 since max for ToA?


number_accuracy = 6 #number of after comma positions

#lora related parameters
payload_bytes = 1
cyclic_redundancy_check = 1
header_enabled = 1
header_length = 20
low_datarate_optimize = 0
coding_rate = 4
preamble_length = 8
bandwidth = 125000
  
#slotted related parameters
#possible time drifts 
ppm_drift = drift_per_second = np.asarray([2,5,10,15,20,25,50,75,100,125,150])
drift_per_second = ppm_drift*0.0036/3600 #0.36: 100ppm per hour
slotted_max_time_drift = drift_per_second * 3600 #360ms as max time drift

#drift randomness
randomness = 0.1
drift_variation = np.linspace(0,randomness,1000)

#max toa (sf12, 51 byte)
max_toa = 3.023

drift_guard_time = slotted_max_time_drift*k_exact
sync_length = 6 #B
sf = [7,8,9,10,11,12]

#get toa of sync with 6B
sync_packet = (8 * sync_length - (4*np.array(sf)) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * np.array(sf) - 2*low_datarate_optimize)
n_sync_packet = 8 + (np.ceil(sync_packet)* (coding_rate + 4))
total_sync_symbols = preamble_length + 4.25 + n_sync_packet
symbol_duration = (2**np.array(sf))/bandwidth
sync_toa = symbol_duration * total_sync_symbols

sync_sf_12 = sync_toa[5]

#get slot length and thus, number of possible messages
slot_lengths = drift_guard_time + sync_toa[5] + max_toa + slotted_max_time_drift + slotted_max_time_drift*randomness
max_messages = 3600/slot_lengths

def collision_calc(dataframe, threshold, curr_simhour):
    #collision check
 
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
    for m in range(len(dataframe['transmission_starts'])-1):
        #check if drift exceeds limit   
        if dataframe['transmission_starts'][m+1] < dataframe['transmission_ends'][m]:
            
            if (dataframe['message_type'][m+1] + dataframe['message_type'][m] == 0):
                if dataframe['spreading_factor'][m+1] > dataframe['spreading_factor'][m]:
                    dataframe['systematic_collisions'][m] = 1
                elif dataframe['spreading_factor'][m+1] < dataframe['spreading_factor'][m]:
                    dataframe['systematic_collisions'][m+1] = 1
                else:
                    dataframe['systematic_collisions'][m] = 1
                    dataframe['systematic_collisions'][m + 1] = 1
            else:
                if dataframe['spreading_factor'][m+1] > dataframe['spreading_factor'][m]:
                    dataframe['crosstraffic_collisions'][m] = 1
                elif dataframe['spreading_factor'][m+1] < dataframe['spreading_factor'][m]:
                    dataframe['crosstraffic_collisions'][m+1] = 1
                else:
                    dataframe['crosstraffic_collisions'][m] = 1
                    dataframe['crosstraffic_collisions'][m + 1] = 1
            
            
        if dataframe['current_time_drift'][m] > threshold:
            #check if packet lost
            if (dataframe['systematic_collisions'][m] == 0) & (dataframe['crosstraffic_collisions'][m]==0):
                #check if sync lost
                sync_collision = np.where((dataframe['transmission_starts'] >dataframe['transmission_ends'][m]) & (dataframe['transmission_starts'] < (dataframe['transmission_ends'][m] + sync_sf_12))) #
                if len(sync_collision[0]) == 0:
                    dataframe['transmission_starts'][m] = dataframe['transmission_starts'][m] - dataframe['current_time_drift'][m]
                    dataframe['last_sync_time'][m]  = dataframe['transmission_ends'][m] 
                    dataframe['transmission_ends'][m] = dataframe['transmission_ends'][m] - dataframe['current_time_drift'][m]
                    dataframe['current_time_drift'][m] = 0
                    dataframe['numbersyncs'][m] = 1
                elif dataframe['spreading_factor'][m] < 12: 
                    dataframe['transmission_starts'][m] = dataframe['transmission_starts'][m] - dataframe['current_time_drift'][m]
                    dataframe['last_sync_time'][m]  = dataframe['transmission_ends'][m] 
                    dataframe['transmission_ends'][m] = dataframe['transmission_ends'][m] - dataframe['current_time_drift'][m]
                    dataframe['current_time_drift'][m] = 0
                    dataframe['numbersyncs'][m] =  1
                    dataframe['crosstraffic_collisions'][m+1] = 1
                else:
                    dataframe['lost_syncs'][m] = 1
                    dataframe['crosstraffic_collisions'][m+1] = 1
            
    m = m + 1            
    if dataframe['current_time_drift'][m] > threshold:
        #check if packet lost
        if (dataframe['systematic_collisions'][m] == 0) & (dataframe['crosstraffic_collisions'][m]==0):
            #check if sync lost
            sync_collision = np.where((dataframe['transmission_starts'] >dataframe['transmission_ends'][m]) & (dataframe['transmission_starts'] < (dataframe['transmission_ends'][m] + sync_sf_12)))
            if len(sync_collision[0]) == 0:
                dataframe['transmission_starts'][m] = dataframe['transmission_starts'][m] - dataframe['current_time_drift'][m]
                dataframe['last_sync_time'][m]  = dataframe['transmission_ends'][m] 
                dataframe['transmission_ends'][m] = dataframe['transmission_ends'][m] - dataframe['current_time_drift'][m]
                dataframe['current_time_drift'][m] = 0
                dataframe['numbersyncs'][m] =  1
            elif dataframe['spreading_factor'][m] < 12: 
                dataframe['transmission_starts'][m] = dataframe['transmission_starts'][m] - dataframe['current_time_drift'][m]
                dataframe['last_sync_time'][m]  = dataframe['transmission_ends'][m] 
                dataframe['transmission_ends'][m] = dataframe['transmission_ends'][m] - dataframe['current_time_drift'][m]
                dataframe['current_time_drift'][m] = 0
                dataframe['numbersyncs'][m] =  1
            else:
                dataframe['lost_syncs'][m] = 1
    
    all_slotted_collisions = 0
    tmp_messagetypes = dataframe['message_type']
    all_crosstraffic_collisions = np.sum(tmp_messagetypes[np.where(dataframe['crosstraffic_collisions'])[0]])
    all_systematic_collisions = np.sum(dataframe['systematic_collisions'])
    all_slotted_collisions = np.sum(dataframe['crosstraffic_collisions']) - all_crosstraffic_collisions
    all_synclosses = np.sum(dataframe['lost_syncs'])
    all_syncs = np.sum(dataframe['numbersyncs'])
    all_collisions = all_crosstraffic_collisions + all_slotted_collisions + all_systematic_collisions
    
    
    #todo reset collisions and syncs 
    dataframe['systematic_collisions'] = 0
    dataframe['crosstraffic_collisions'] = 0
    dataframe['lost_syncs'] = 0
    dataframe['numbersyncs'] = 0
    
    #next hour traffic
    #crosstraffic
    number_messages_crosstraffic = len((np.where(dataframe['message_type'] == 1))[0])
    number_messages_slotted = len((np.where(dataframe['message_type'] == 0))[0])

    all_crosstraffic_collisions = all_crosstraffic_collisions/number_messages_crosstraffic
    all_systematic_collisions = all_systematic_collisions/number_messages_slotted
    all_slotted_collisions = all_slotted_collisions/number_messages_slotted
    all_collisions = all_collisions/(number_messages_slotted+number_messages_crosstraffic)
    all_synclosses = all_synclosses/number_messages_slotted
    all_syncs = all_syncs/number_messages_slotted
    
    spreading_factor_crosstraffic = np.random.randint(6,size=number_messages_crosstraffic)+7
    #sensor_dataframe['spreading_factor'] = spreading_factor
    
    payload_crosstraffic = np.random.randint(payload_max,size=number_messages_crosstraffic)+payload_min
    #sensor_dataframe['payload'] = payload
        
    #time on air calculation
    all_packet = (8 * payload_crosstraffic - (4*spreading_factor_crosstraffic) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * spreading_factor_crosstraffic - 2*low_datarate_optimize)
    n_packet = 8 + (np.ceil(all_packet)* (coding_rate + 4))
    total_symbols = preamble_length + 4.25 + n_packet
    symbol_duration = (2**spreading_factor_crosstraffic)/bandwidth
    toa_crosstraffic = symbol_duration * total_symbols
    
    dataframe = dataframe.sort_values('index',ignore_index=True)
    all_transmission_starts = dataframe['transmission_starts']
    all_transmission_ends = dataframe['transmission_ends']
    all_transmission_toas = dataframe['time_on_air']
    all_transmission_sfs = dataframe['spreading_factor']
    all_transmission_payload = dataframe['payload']
    
    transmission_starts_slotted = all_transmission_starts[np.where(dataframe['message_type'] == 0)[0]] + 3600
    transmission_ends_slotted = all_transmission_ends[np.where(dataframe['message_type'] == 0)[0]]  + 3600
    
    toa_slotted = all_transmission_toas[np.where(dataframe['message_type'] == 0)[0]] 
    sf_slotted = all_transmission_sfs[np.where(dataframe['message_type'] == 0)[0]] 
    payload_slotted = all_transmission_payload[np.where(dataframe['message_type'] == 0)[0]] 
    
    transmission_starts_crosstraffic = np.random.uniform(0, 3600, size=(number_messages_crosstraffic,)) + (curr_simhour+1) * 3600
    transmission_ends_crosstraffic = transmission_starts_crosstraffic + toa_crosstraffic
    
    dataframe['transmission_starts'] = np.concatenate((transmission_starts_slotted,transmission_starts_crosstraffic),axis=0)
    dataframe['transmission_ends'] = np.concatenate((transmission_ends_slotted,transmission_ends_crosstraffic),axis=0)
    dataframe['time_on_air'] = np.concatenate((toa_slotted,toa_crosstraffic),axis=0)
    dataframe['spreading_factor'] = np.concatenate((sf_slotted,spreading_factor_crosstraffic),axis=0)
    dataframe['payload'] = np.concatenate((payload_slotted,payload_crosstraffic),axis=0)


    return [all_syncs, all_synclosses, all_crosstraffic_collisions, all_systematic_collisions, all_slotted_collisions, all_collisions, dataframe]
  
#last sync - letztes mal simuliert, current time - momentane startzeit, behavior 80/60/10 ppm, random drift vs. immer gleicher
#drift (drift up to 20ppm, schwankung um den "m"-Wert)
def calculate_clock_drift(dataframe, drift):
    #t = 5.4
    error_direction = np.random.randint(2, size=len(dataframe))
    error_direction[np.where(error_direction == 0)] = -1
    difference = dataframe['transmission_starts'] - dataframe['last_sync_time']
    
    drift_error_index = np.random.randint(1000, size=len(dataframe)) 
    
    #next_drift_tmp = (dataframe['driftbehavior'] * difference * 1000 + t)/1000
    next_drift_tmp = dataframe['drift_per_second'] * difference

    next_drift_error = drift_variation[drift_error_index] * error_direction
    
    next_drift_tmp = next_drift_tmp + next_drift_tmp * next_drift_error
    
    drift_diff = next_drift_tmp - dataframe['current_time_drift'] 
    dataframe['current_time_drift'] =  next_drift_tmp
    dataframe['transmission_starts'] = dataframe['transmission_starts'] + drift_diff
    dataframe['transmission_ends'] = dataframe['transmission_ends'] + drift_diff
    return dataframe

#%%
all_syncs_array = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
all_synclosses_array = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
all_crosstraffic_collisions_array = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
all_systematic_collisions_array = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
all_slotted_collisions_array = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
all_collisions_array = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))

#one simulation for each drift
for i in range(len(ppm_drift)):
    print('i = ' + str(i))
    #one sim for each crosstraffic
    for l in range(len(percent_crosstraffic)):
        print('l = ' + str(l))
        current_slotted_messages = number_sensors[i]
        current_crosstraffic = math.ceil(number_sensors[i] * percent_crosstraffic[l]/100)
        all_messages = current_slotted_messages + current_crosstraffic
        
        possible_slots = np.linspace(0,3600,current_slotted_messages)   
        
        sensor_index = np.arange(all_messages)+1
        
        sensor_dataframe = pd.DataFrame({'index': sensor_index})
        #sensor_dataframe['transmission_attempts'] = np.ones(number_sensors)
        
        spreading_factor = np.random.randint(6,size=all_messages)+7
        sensor_dataframe['spreading_factor'] = spreading_factor
        
        payload = np.random.randint(payload_max,size=all_messages)+payload_min
        sensor_dataframe['payload'] = payload
            
        #time on air calculation
        all_packet = (8 * sensor_dataframe['payload'] - (4*sensor_dataframe['spreading_factor']) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * sensor_dataframe['spreading_factor'] - 2*low_datarate_optimize)
        n_packet = 8 + (np.ceil(all_packet)* (coding_rate + 4))
        total_symbols = preamble_length + 4.25 + n_packet
        symbol_duration = (2**sensor_dataframe['spreading_factor'])/bandwidth
        sensor_dataframe['time_on_air'] = symbol_duration * total_symbols
        
        #one sim for each drift setting, new start times
        for k in range(number_drift_reconfigs):
            print('k = ' + str(k))
            slotted_transmission_starts = possible_slots[random.sample(range(0, len(possible_slots)), current_slotted_messages)]
            crosstraffic_transmission_starts = np.random.uniform(0, 3600, size=(current_crosstraffic,))
            sensor_dataframe['transmission_starts'] = np.concatenate((slotted_transmission_starts,crosstraffic_transmission_starts),axis=0)
            sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_starts'] + sensor_dataframe['time_on_air']
            current_drift_slotted = np.zeros(current_slotted_messages) + np.random.uniform(0, drift_guard_time[i], size=(current_slotted_messages,))
            sensor_dataframe['current_time_drift'] = np.concatenate((current_drift_slotted,np.zeros(current_crosstraffic)),axis=0)
            sensor_dataframe['last_sync_time'] = np.zeros(all_messages)
            
            sensor_dataframe['transmission_starts'] = sensor_dataframe['transmission_starts'] + sensor_dataframe['current_time_drift']
            sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_ends'] + sensor_dataframe['current_time_drift']
            #0: sensor message slotted, 1: sensor message randomaccess, 2: gw message
            messagetype_slotted = np.zeros(current_slotted_messages) 
            messagetype_crosstraffic = np.ones(current_crosstraffic)       
            sensor_dataframe['message_type'] = np.concatenate((messagetype_slotted,messagetype_crosstraffic),axis=0)
            
            sensor_dataframe['crosstraffic_collisions'] = np.zeros(all_messages)
            sensor_dataframe['lost_syncs'] = np.zeros(all_messages)
            sensor_dataframe['systematic_collisions'] = np.zeros(all_messages)
            sensor_dataframe['numbersyncs'] = np.zeros(all_messages)
            
            drift_type_per_second_slotted = np.random.uniform(0, drift_per_second[i], size=(current_slotted_messages,))
            sensor_dataframe['drift_per_second'] = np.concatenate((drift_type_per_second_slotted,np.zeros(current_crosstraffic)),axis=0)
            for j in range(sim_repetitions):
                #print(j)
                [all_syncs_array[i][l][k][j], all_synclosses_array[i][l][k][j], all_crosstraffic_collisions_array[i][l][k][j], all_systematic_collisions_array[i][l][k][j], all_slotted_collisions_array[i][l][k][j], all_collisions_array[i][l][k][j], sensor_dataframe] = collision_calc(sensor_dataframe, drift_guard_time[i], j) #full dataframe to function if all sensors use aloha               
                sensor_dataframe = calculate_clock_drift(sensor_dataframe, drift_per_second[i])
                #if j == sim_repetitions-2:
                #    print('there')

np.save('all_syncs_array_sfrecovery', all_syncs_array)
np.save('all_synclosses_array_sfrecovery', all_synclosses_array)
np.save('all_crosstraffic_collisions_array_sfrecovery', all_crosstraffic_collisions_array)
np.save('all_systematic_collisions_array_array_sfrecovery', all_systematic_collisions_array)
np.save('all_slotted_collisions_array_sfrecovery', all_slotted_collisions_array)
np.save('all_collisions_array_sfrecovery', all_collisions_array)
