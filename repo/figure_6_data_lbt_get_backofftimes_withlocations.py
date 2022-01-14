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
import math
import random

#sim input
number_sensors = np.arange(2500)+1
sim_repetitions = 5

#payload distribution
payload_distribution = 'random' #todo exponential more likely?
payload_min = 1
payload_max = 51 #todo others - 50 since max for ToA?


number_accuracy = 6 #number of after comma positions

#channel access
channel_access = 'lbt' #possible: aloha; slotted; lbt; other (any other or selective strategy)
number_channels = 1
channel_selection = 'random' #tbt - other?
backoff_strategy = 'all' #todo 'random' - all tests all possible combinations


gw_height = 3
sf = [7,8,9,10,11,12]
sens_height = 3
plrange = [131, 134, 137, 140, 141, 144]

#lora related parameters
payload_bytes = 1
cyclic_redundancy_check = 1
header_enabled = 1
header_length = 20
low_datarate_optimize = 0
coding_rate = 4
preamble_length = 8
bandwidth = 125000


def listen_before_talk(dataframe, sensors):
    #collision check
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
    i = 0
    backshift_time = 0
    while i < sensors-2:
        j = i + 1
        while(j < sensors and dataframe['transmission_starts'][j] < dataframe['transmission_starts'][i] + 10):
            backoff_random = np.round(np.random.uniform(low = 0.4, high=1.75, size=1), number_accuracy)
            
            if dataframe['transmission_starts'][j] < dataframe['transmission_ends'][i]:
                sensor_dist = math.dist([dataframe['sensor_x'][i], dataframe['sensor_y'][i]],[dataframe['sensor_x'][i+1], dataframe['sensor_y'][i+2]])
                
                #get sf of first sensorand transmission dist of it         
                possible_dist = distances[int(dataframe['spreading_factor'][i]-7)]
    
                if possible_dist > sensor_dist: 
                    #sensors in range
                    dataframe['transmission_starts'][j] = dataframe['transmission_starts'][j] + backoff_random
                    dataframe['transmission_ends'][j] = dataframe['transmission_ends'][j] + backoff_random
                    dataframe['transmission_attempts'][j] = dataframe['transmission_attempts'][j] + 1
                    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
                    backshift_time = backshift_time + backoff_random
                    i = i - 1
                else: 
                    #sensors not in range; assume both lost
                    #todo: additional error correction 
                    dataframe['collisions'][i] = 1
                    dataframe['collisions'][j] = 1   
            
            j = j + 1
                
        i = i + 1
    backshifts = np.sum(dataframe['transmission_attempts']) - sensors
    number_shifted_sensors = np.size(np.where(dataframe['transmission_attempts']>1))
    collisions = np.sum(dataframe['collisions'])
    avg_backshift_time = backshift_time/sensors
    return [backshifts, number_shifted_sensors, collisions, avg_backshift_time, dataframe]
  
all_backshifts = np.zeros((len(number_sensors),sim_repetitions))
number_shifted_sensors = np.zeros((len(number_sensors),sim_repetitions))
collision_array = np.zeros((len(number_sensors),sim_repetitions))
number_carryovers = np.zeros((len(number_sensors),sim_repetitions))
avg_shifted_time = np.zeros((len(number_sensors),sim_repetitions))


distances = np.zeros(len(sf))
for i in range(len(sf)):
    distance = 10**(-(74.52+76.8291993990029-13.82*math.log10(gw_height)-3.2*(math.log10(11.75*sens_height)**2)-plrange[sf[i]-7])/(44.9-6.55*math.log10(gw_height)))
    distances[i] = distance*1000
  

#get maximal distance to x and y coordinates dependent on max distance from hata model; create more points than needed
tmp_x = np.random.randint(distances[len(distances)-1] * 2, size=20000)
tmp_y = np.random.randint(distances[len(distances)-1] * 2, size=20000)

#calc dist to potential gateway 

########## fix code here - dist calculation wrong!!!!!!
#get reachable sensors by max dist with sf12 
dists = np.zeros(len(tmp_x))
for i in range(len(tmp_x)):
    #dists[i] = math.dist([tmp_x[i], distances[len(distances)-1]],[tmp_y[i], distances[len(distances)-1]])
    dists[i] = math.dist([0,0],[tmp_x[i],tmp_y[i]])
    
#get possible dists, x and y coordinates
dists = dists[np.where(dists<distances[len(distances)-1])]
sensor_x_tmp = tmp_x[np.where(dists<distances[len(distances)-1])]
sensor_y_tmp = tmp_y[np.where(dists<distances[len(distances)-1])]


for i in range(len(number_sensors)):
    carryover_dataframe = []
    for j in range(sim_repetitions):
        print("i = " + str(i))
        print("j = " + str(j))
        
        sensor_index = np.arange(number_sensors[i])+1

        sensor_dataframe = pd.DataFrame({'index': sensor_index})
        sensor_dataframe['transmission_attempts'] = np.ones(number_sensors[i])
        
        current_sensorslocations = random.sample(range(0, len(dists)), number_sensors[i])
        
        sensor_dist = dists[current_sensorslocations]
    
        sensor_x = sensor_x_tmp[current_sensorslocations]
        sensor_y = sensor_y_tmp[current_sensorslocations]
        
        #set sf distribution
        sensor_dataframe['sensor_x'] = sensor_x
        sensor_dataframe['sensor_y'] = sensor_y
        sensor_dataframe['sensor_dist'] = sensor_dist
            
        spreading_factor = np.zeros(number_sensors[i])
        
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


        
        payload = np.random.randint(payload_max,size=number_sensors[i])+payload_min
        sensor_dataframe['payload'] = payload
            
        #time on air calculation
        all_packet = (8 * sensor_dataframe['payload'] - (4*sensor_dataframe['spreading_factor']) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * sensor_dataframe['spreading_factor'] - 2*low_datarate_optimize)
        n_packet = 8 + (np.ceil(all_packet)* (coding_rate + 4))
        total_symbols = preamble_length + 4.25 + n_packet
        symbol_duration = (2**sensor_dataframe['spreading_factor'])/bandwidth
        sensor_dataframe['time_on_air'] = symbol_duration * total_symbols


        sensor_dataframe['transmission_starts'] = np.round(np.random.uniform(low = 0, high=3600, size=number_sensors[i]), number_accuracy)
        sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_starts'] + sensor_dataframe['time_on_air']
        sensor_dataframe['collisions'] = np.zeros(number_sensors[i])

        sensor_dataframe = sensor_dataframe.append(carryover_dataframe)

        [all_backshifts[i][j], number_shifted_sensors[i][j], collision_array[i][j], avg_shifted_time[i][j], sensor_dataframe] = listen_before_talk(sensor_dataframe, number_sensors[i]) #full dataframe to function if all sensors use aloha
        carryover_dataframe = sensor_dataframe[sensor_dataframe['transmission_ends'] > 3600] 
        carryover_dataframe['transmission_starts'] = carryover_dataframe['transmission_starts'] - 3600
        carryover_dataframe['transmission_ends'] = carryover_dataframe['transmission_ends'] - 3600
        
        number_carryovers[i][j] = np.size(carryover_dataframe['transmission_ends'])
        
    #%%
results = pd.DataFrame({'index': number_sensors})
results['all_backshifts'] = np.mean(all_backshifts,axis=1)
results['number_sensors_shifted'] = np.mean(number_shifted_sensors,axis=1)
results['collisions'] = np.mean(collision_array,axis=1)
results['carryovers'] = np.mean(number_carryovers, axis=1)
results['avg_shifted_time'] = np.mean(avg_shifted_time, axis=1)

results.to_csv('lbt_backshift_by_sensornumber_location.csv')    




