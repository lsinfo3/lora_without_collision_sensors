#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 17:53:39 2021

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


gw_height = 3
sf = [7,8,9,10,11,12]
sens_height = 3
plrange = [131, 134, 137, 140, 141, 144]
distances = np.zeros(len(sf))
for i in range(len(sf)):
    distance = 10**(-(74.52+76.8291993990029-13.82*math.log10(gw_height)-3.2*(math.log10(11.75*sens_height)**2)-plrange[sf[i]-7])/(44.9-6.55*math.log10(gw_height)))
    distances[i] = distance*1000

def collision_calc(dataframe, threshold, curr_simhour):
    #collision check
 
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
    m = 0
    backshift_time = 0
    while m < len(dataframe['transmission_starts'])-1:
        backoff_random = np.round(np.random.uniform(low = 0.4, high=1.75, size=1), number_accuracy)[0]
        tmp_backoff = 0
        #check if drift exceeds limit   
        if dataframe['transmission_starts'][m+1] < dataframe['transmission_ends'][m]:
            #message type == 0, thus slotted, thus collision
            if dataframe['message_type'][m+1] == 0:
                if (dataframe['message_type'][m+1] + dataframe['message_type'][m] == 0):
                    dataframe['systematic_collisions'][m] = 1
                    dataframe['systematic_collisions'][m + 1] = 1
                else:
                    dataframe['crosstraffic_collisions'][m] = 1
                    dataframe['crosstraffic_collisions'][m + 1] = 1
                    
            else:
                sensor_dist = math.dist([dataframe['sensor_x'][m], dataframe['sensor_y'][m]],[dataframe['sensor_x'][m+1], dataframe['sensor_y'][m+1]])
                    
                #get sf of first sensorand transmission dist of it         
                possible_dist = distances[int(dataframe['spreading_factor'][m]-7)]
    
                if possible_dist > sensor_dist: 
                    #sensors in range
                    dataframe['transmission_starts'][m+1] = dataframe['transmission_starts'][m+1] + backoff_random
                    dataframe['transmission_ends'][m+1] = dataframe['transmission_ends'][m+1] + backoff_random
                    dataframe['transmission_attempts'][m+1] = dataframe['transmission_attempts'][m+1] + 1
                    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
                    backshift_time = backshift_time + backoff_random
                    tmp_backoff = -1
                else: 
                    #sensors not in range; assume both lost
                    #todo: additional error correction 
                    dataframe['crosstraffic_collisions'][m] = 1
                    dataframe['crosstraffic_collisions'][m+1] = 1  
            
            
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
                elif len(sync_collision[0]) == 1: 
                    if dataframe['message_type'][m+1] == 0:
                        dataframe['lost_syncs'][m] =  1
                        dataframe['crosstraffic_collisions'][m+1] = 1
                    else:
                        dataframe['transmission_starts'][m] = dataframe['transmission_starts'][m] - dataframe['current_time_drift'][m]
                        dataframe['last_sync_time'][m]  = dataframe['transmission_ends'][m] 
                        dataframe['transmission_ends'][m] = dataframe['transmission_ends'][m] - dataframe['current_time_drift'][m]
                        dataframe['current_time_drift'][m] = 0
                        dataframe['numbersyncs'][m] = 1
                        dataframe['transmission_starts'][m+1] = dataframe['transmission_starts'][m+1] + backoff_random
                        dataframe['transmission_ends'][m+1] = dataframe['transmission_ends'][m+1] + backoff_random
                        dataframe['transmission_attempts'][m+1] = dataframe['transmission_attempts'][m+1] + 1
                        dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
                        backshift_time = backshift_time + backoff_random
                else:
                    dataframe['lost_syncs'][m] =  1
                    dataframe['crosstraffic_collisions'][m+1] = 1
                        
                        
            
                
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
                else: 
                    dataframe['lost_syncs'][m] = 1
        m = m + 1 + tmp_backoff
                
                
    all_slotted_collisions = 0
    tmp_messagetypes = dataframe['message_type']
    all_crosstraffic_collisions = np.sum(tmp_messagetypes[np.where(dataframe['crosstraffic_collisions'])[0]])
    all_slotted_collisions = np.sum(dataframe['crosstraffic_collisions']) - all_crosstraffic_collisions  
    all_systematic_collisions = np.sum(dataframe['systematic_collisions'])
    all_synclosses = np.sum(dataframe['lost_syncs'])
    all_syncs = np.sum(dataframe['numbersyncs'])
    all_collisions = all_crosstraffic_collisions + all_slotted_collisions + all_systematic_collisions


    percent_backshift = (np.sum(dataframe['transmission_attempts']) - len(dataframe['transmission_starts']))
    percent_sensors_backshift = (np.size(np.where(dataframe['transmission_attempts']>1)))
    avg_backshift_time = backshift_time/len(dataframe['transmission_starts'])
    
    #todo reset collisions and syncs 
    dataframe['systematic_collisions'] = 0
    dataframe['crosstraffic_collisions'] = 0
    dataframe['lost_syncs'] = 0
    dataframe['numbersyncs'] = 0
    sensor_dataframe['transmission_attempts'] = 1
    
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
    percent_backshift = percent_backshift/number_messages_crosstraffic
    percent_sensors_backshift = percent_sensors_backshift/number_messages_crosstraffic
    avg_backshift_time = avg_backshift_time/number_messages_crosstraffic
    
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


    return [percent_backshift, percent_sensors_backshift, all_syncs, all_synclosses, all_crosstraffic_collisions, all_systematic_collisions, all_slotted_collisions, all_collisions, avg_backshift_time, dataframe]
  
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



percent_backshift = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
percent_sensors_backshift = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))
avg_backshift_time = np.zeros((len(ppm_drift),len(percent_crosstraffic),number_drift_reconfigs,sim_repetitions))

#one simulation for each drift
for i in range(len(ppm_drift)):
    print('i = ' + str(i/len(ppm_drift)))
    #one sim for each crosstraffic
    for l in range(len(percent_crosstraffic)):
        print('l = ' + str(l/len(percent_crosstraffic)))

        tmp_x = np.random.randint(distances[len(distances)-1] * 2, size=20000)
        tmp_y = np.random.randint(distances[len(distances)-1] * 2, size=20000)
        
        #calc dist to potential gateway 
        
        
        #get reachable sensors by max dist with sf12 
        dists = np.zeros(len(tmp_x))
        for m in range(len(tmp_x)):
            dists[m] = math.dist([tmp_x[m], distances[len(distances)-1]],[tmp_y[m], distances[len(distances)-1]])
            
        #get possible dists, x and y coordinates
        dists = dists[np.where(dists<distances[len(distances)-1])]
        sensor_x_tmp = tmp_x[np.where(dists<distances[len(distances)-1])]
        sensor_y_tmp = tmp_y[np.where(dists<distances[len(distances)-1])]
        
        
        current_slotted_messages = number_sensors[i]
        current_crosstraffic = math.ceil(number_sensors[i] * percent_crosstraffic[l]/100)
        all_messages = current_slotted_messages + current_crosstraffic
        
        possible_slots = np.linspace(0,3600-slot_lengths[i],current_slotted_messages)   
        
        sensor_index = np.arange(all_messages)+1
        
        sensor_dataframe = pd.DataFrame({'index': sensor_index})
        
        sensor_dataframe['transmission_attempts'] = np.ones(all_messages)
        
                    
        current_sensorslocations = random.sample(range(0, len(dists)), int(all_messages))
        
        sensor_dist = dists[current_sensorslocations]
    
        sensor_x = sensor_x_tmp[current_sensorslocations]
        sensor_y = sensor_y_tmp[current_sensorslocations]
                #set sf distribution
        sensor_dataframe['sensor_x'] = sensor_x
        sensor_dataframe['sensor_y'] = sensor_y
        sensor_dataframe['sensor_dist'] = sensor_dist
            
        spreading_factor = np.zeros(int(all_messages))
        
        spreading_factor[np.where(sensor_dataframe['sensor_dist']  < distances[0])] = 7
        boolean_array = np.logical_and(sensor_dataframe['sensor_dist'] >=distances[0], sensor_dataframe['sensor_dist'] < distances[1])
        spreading_factor[np.where(boolean_array)[0]] = 8
        
        boolean_array = np.logical_and(sensor_dataframe['sensor_dist'] >=distances[1], sensor_dataframe['sensor_dist'] < distances[2])
        spreading_factor[np.where(boolean_array)[0]] = 9
        
        boolean_array = np.logical_and(sensor_dataframe['sensor_dist'] >=distances[2], sensor_dataframe['sensor_dist'] < distances[3])
        spreading_factor[np.where(boolean_array)[0]] = 10
        
        boolean_array = np.logical_and(sensor_dataframe['sensor_dist'] >=distances[3], sensor_dataframe['sensor_dist'] < distances[4])
        spreading_factor[np.where(boolean_array)[0]] = 11
        
        boolean_array = np.logical_and(sensor_dataframe['sensor_dist'] >=distances[4], sensor_dataframe['sensor_dist'] < distances[5])
        spreading_factor[np.where(boolean_array)[0]] = 12
        
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
                [percent_backshift[i][l][k][j], percent_sensors_backshift[i][l][k][j], all_syncs_array[i][l][k][j], all_synclosses_array[i][l][k][j], all_crosstraffic_collisions_array[i][l][k][j], all_systematic_collisions_array[i][l][k][j], all_slotted_collisions_array[i][l][k][j], all_collisions_array[i][l][k][j], avg_backshift_time[i][l][k][j], sensor_dataframe] = collision_calc(sensor_dataframe, drift_guard_time[i], j) #full dataframe to function if all sensors use aloha               
                
                sensor_dataframe = calculate_clock_drift(sensor_dataframe, drift_per_second[i])




np.save('all_syncs_slotted_lbt_no_recovery', all_syncs_array)
np.save('all_synclosses_slotted_lbt_no_recovery', all_synclosses_array)
np.save('all_crosstraffic_collisions_slotted_lbt_no_recovery', all_crosstraffic_collisions_array)
np.save('all_systematic_collisions_slotted_lbt_no_recovery', all_systematic_collisions_array)
np.save('all_slotted_collisions_slotted_lbt_no_recovery', all_slotted_collisions_array)
np.save('all_collisions_slotted_lbt_no_recovery', all_collisions_array)

np.save('percent_backshift_total_slotted_lbt_no_recovery', percent_backshift)
np.save('percent_sensors_backshift_slotted_lbt_no_recovery', percent_sensors_backshift)
np.save('avg_backshift_time__slotted_lbt_no_recovery', avg_backshift_time)
