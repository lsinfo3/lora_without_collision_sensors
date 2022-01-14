#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 15:17:18 2021

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
import math
import random

#sim input
number_sensors = np.arange(1500)+1
sim_repetitions = 10
collision_result_array = np.zeros((len(number_sensors), sim_repetitions))
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

distances = np.zeros(len(sf))
for i in range(len(sf)):
    distance = 10**(-(74.52+76.8291993990029-13.82*math.log10(gw_height)-3.2*(math.log10(11.75*sens_height)**2)-plrange[sf[i]-7])/(44.9-6.55*math.log10(gw_height)))
    distances[i] = distance*1000

#%%
def random_access(dataframe, curr_sensors):
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)

    for i in range(curr_sensors-1):
        j = i + 1
        while(j < curr_sensors and dataframe['transmission_starts'][j] < dataframe['transmission_starts'][i] + 10):
        
            if dataframe['transmission_starts'][j] < dataframe['transmission_ends'][i]:
    
                dataframe['collisions'][i] = 1
                dataframe['collisions'][j] = 1
            
            j = j + 1
            
    return np.sum(dataframe['collisions'])

for i in range(len(number_sensors)):
    print("i = " + str(i/1500))
    for j in range(sim_repetitions):       

        tmp_x = np.random.randint(distances[len(distances)-1] * 2, size=20000)
        tmp_y = np.random.randint(distances[len(distances)-1] * 2, size=20000)
        
        #calc dist to potential gateway 
        
        
        #get reachable sensors by max dist with sf12 
        dists = np.zeros(len(tmp_x))
        for m in range(len(tmp_x)):
            #dists[m] = math.dist([tmp_x[m], distances[len(distances)-1]],[tmp_y[m], distances[len(distances)-1]])
            dists[m] = math.dist([0,0],[tmp_x[m],tmp_y[m]])
            
        #get possible dists, x and y coordinates
        dists = dists[np.where(dists<distances[len(distances)-1])]
        sensor_x_tmp = tmp_x[np.where(dists<distances[len(distances)-1])]
        sensor_y_tmp = tmp_y[np.where(dists<distances[len(distances)-1])]
        sensor_index = np.arange(number_sensors[i])+1
        payload_min = 1
        payload_max = 51 #todo others - 50 since max for ToA?
        
        number_accuracy = 6 #number of after comma positions
        
        
        #dataframe initialization
        sensor_dataframe = pd.DataFrame({'index': sensor_index})
        sensor_dataframe['collisions'] = np.zeros(number_sensors[i])
        #%%
        
        current_sensorslocations = random.sample(range(0, len(dists)), int(number_sensors[i]))
            
        sensor_dist = dists[current_sensorslocations]
    
        sensor_x = sensor_x_tmp[current_sensorslocations]
        sensor_y = sensor_y_tmp[current_sensorslocations]
        
        #set sf distribution
        sensor_dataframe['sensor_x'] = sensor_x
        sensor_dataframe['sensor_y'] = sensor_y
        sensor_dataframe['sensor_dist'] = sensor_dist
            
        spreading_factor = np.zeros(int(number_sensors[i]))
        
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
        collision_result_array[i][j] = random_access(sensor_dataframe, number_sensors[i]) #full dataframe to function if all sensors use aloha
        #%%
plt.plot(number_sensors, np.mean(collision_result_array, axis=1)/(number_sensors - np.mean(collision_result_array, axis=1)))
probability = np.mean(collision_result_array, axis=1)/number_sensors
ticks = np.linspace(0.005,0.30,1500)
messages_per_probab = np.zeros(len(ticks))
for i in range(len(ticks)):
    messages_per_probab[i] = np.size(np.where(probability <= ticks[i]))
    
    
aloha_collision = pd.DataFrame({'number_sensors': number_sensors})
aloha_collision['collision_probability'] = probability
aloha_collision['ticks'] = ticks
aloha_collision['messages_per_colissionprobab'] = messages_per_probab

aloha_collision.to_csv('aloha_collisions_lowerSF.csv')    
    