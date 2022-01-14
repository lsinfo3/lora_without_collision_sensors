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
import sys

#NOTE: Adjust backoff delay and random or constant according to usage goal...

#sim input
number_sensors = 1000
sensor_index = np.arange(number_sensors)+1
sim_repetitions = 5

#sf distribution
sf_distribution = 'random' #possible: 'random', 'distance', todo: exponential; more likely?
#input for distance calc based on hata model

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


#dataframe initialization
sensor_dataframe = pd.DataFrame({'index': sensor_index})
#add number of transmission attempts for collisions

#lora related parameters
payload_bytes = 1
cyclic_redundancy_check = 1
header_enabled = 1
header_length = 20
low_datarate_optimize = 0
coding_rate = 4
preamble_length = 8
bandwidth = 125000


def listen_before_talk(dataframe, backoff):
    #collision check
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
    i = 0
    while i < number_sensors-1:
        if dataframe['transmission_starts'][i+1] < dataframe['transmission_ends'][i]:
            backoff_random = backoff[np.random.randint(len(backoff))]    
            #backoff = (np.random.randint(10)+1) * backoff
            dataframe['transmission_starts'][i+1] = dataframe['transmission_starts'][i+1] + backoff_random
            dataframe['transmission_ends'][i+1] = dataframe['transmission_ends'][i+1] + backoff_random
            dataframe['transmission_attempts'][i+1] = dataframe['transmission_attempts'][i+1] + 1
            dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
            i = i - 1
            
        i = i + 1
    backshifts = np.sum(dataframe['transmission_attempts']) - number_sensors
    max_shifts = np.max(dataframe['transmission_attempts'])
    number_shifted_sensors = np.size(np.where(dataframe['transmission_attempts']>1))
    return [backshifts, max_shifts, number_shifted_sensors, dataframe]

if backoff_strategy == 'all':
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
    possible_backoff_times = np.linspace(0.4,1.75,100)
    
    
all_backshifts = np.zeros((len(possible_backoff_times),sim_repetitions))
max_shifts = np.zeros((len(possible_backoff_times),sim_repetitions))
number_shifted_sensors = np.zeros((len(possible_backoff_times),sim_repetitions))


for i in range(len(possible_backoff_times)):
    carryover_dataframe = []
    for j in range(sim_repetitions):
        print("i = " + str(i))
        print("j = " + str(j))
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


        sensor_dataframe['transmission_starts'] = np.round(np.random.uniform(low = 0, high=3600, size=number_sensors), number_accuracy)
        sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_starts'] + sensor_dataframe['time_on_air']
        sensor_dataframe = sensor_dataframe.append(carryover_dataframe)

        [all_backshifts[i][j], max_shifts[i][j], number_shifted_sensors[i][j], sensor_dataframe] = listen_before_talk(sensor_dataframe, possible_backoff_times) #full dataframe to function if all sensors use aloha
        carryover_dataframe = sensor_dataframe[sensor_dataframe['transmission_ends'] > 3600] 
        
#%%
export_data = pd.DataFrame(columns=['backoffs','run1','run2','run3','run4','run5'])
export_data['backoffs'] = possible_backoff_times
export_data['run1'] = all_backshifts[:,0]
export_data['run2'] = all_backshifts[:,1]
export_data['run3'] = all_backshifts[:,2]
export_data['run4'] = all_backshifts[:,3]
export_data['run5'] = all_backshifts[:,4]

export_data['max_shifts1'] = max_shifts[:,0]
export_data['max_shifts2'] = max_shifts[:,1]
export_data['max_shifts3'] = max_shifts[:,2]
export_data['max_shifts4'] = max_shifts[:,3]
export_data['max_shifts5'] = max_shifts[:,4]

export_data['number_sensors_shifted1'] = number_shifted_sensors[:,0]
export_data['number_sensors_shifted2'] = number_shifted_sensors[:,1]
export_data['number_sensors_shifted3'] = number_shifted_sensors[:,2]
export_data['number_sensors_shifted4'] = number_shifted_sensors[:,3]
export_data['number_sensors_shifted5'] = number_shifted_sensors[:,4]

export_data.to_csv('backoff_random_smallrange_1000sensors.csv')

