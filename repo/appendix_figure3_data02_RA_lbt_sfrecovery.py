#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 11:13:23 2021

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
pd.options.mode.chained_assignment = None

#sim input
number_sensors = np.arange(77)*25+100
sim_repetitions = 200

percent_crosstraffic = [0,1,2,3,5,10,15,20,25,30,40,50,60,70,75,80,85,90,95,97,98,99,100]

#payload distribution
payload_distribution = 'random' #todo exponential more likely?
payload_min = 1
payload_max = 51 #todo others - 50 since max for ToA?


number_accuracy = 6 #number of after comma positions

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



def listen_before_talk(dataframe, sensors):
    #collision check
    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
    i = 0
    backshift_time = 0
    number_lbt_sensors = len(np.where(dataframe['access_type'] ==0)[0])
    number_ra_sensors = len(np.where(dataframe['access_type'] ==1)[0])

    while i < sensors-2:
        backoff_random = np.round(np.random.uniform(low = 0.4, high=1.75, size=1), number_accuracy)[0]
        
        if dataframe['transmission_starts'][i+1] < dataframe['transmission_ends'][i]:
            #second message is RA
            if dataframe['access_type'][i+1] == 1:
                if dataframe['spreading_factor'][i+1] > dataframe['spreading_factor'][i]:
                    dataframe['collisions'][i] = 1
                elif dataframe['spreading_factor'][i+1] < dataframe['spreading_factor'][i]:
                    dataframe['collisions'][i+1] = 1
                else:
                    dataframe['collisions'][i] = 1
                    dataframe['collisions'][i + 1] = 1      
            #second message is LBT
            else:
                sensor_dist = math.dist([dataframe['sensor_x'][i], dataframe['sensor_y'][i]],[dataframe['sensor_x'][i+1], dataframe['sensor_y'][i+1]])
                
                #get sf of first sensorand transmission dist of it         
                possible_dist = distances[int(dataframe['spreading_factor'][i]-7)]
    
                if possible_dist > sensor_dist: 
                    #sensors in range
                    dataframe['transmission_starts'][i+1] = dataframe['transmission_starts'][i+1] + backoff_random
                    dataframe['transmission_ends'][i+1] = dataframe['transmission_ends'][i+1] + backoff_random
                    dataframe['transmission_attempts'][i+1] = dataframe['transmission_attempts'][i+1] + 1
                    dataframe = dataframe.sort_values('transmission_starts',ignore_index=True)
                    backshift_time = backshift_time + backoff_random
                    i = i - 1
                else: 
                    #sensors not in range; assume both lost
                    #todo: additional error correction 
                    if dataframe['spreading_factor'][i+1] > dataframe['spreading_factor'][i]:
                        dataframe['collisions'][i] = 1
                    elif dataframe['spreading_factor'][i+1] < dataframe['spreading_factor'][i]:
                        dataframe['collisions'][i+1] = 1
                    else:
                        dataframe['collisions'][i] = 1
                        dataframe['collisions'][i + 1] = 1                       
            
        i = i + 1
    percent_backshift = (np.sum(dataframe['transmission_attempts']) - sensors)/sensors
    percent_sensors_backshift = (np.size(np.where(dataframe['transmission_attempts']>1)))/sensors
    all_collision_array = dataframe['collisions']
    percent_allcollisions = (np.sum(all_collision_array))/sensors
    if number_lbt_sensors > 0:
        percent_lbt_collisions = np.sum(all_collision_array[np.where(dataframe['access_type'] ==0)[0]])/number_lbt_sensors
    else: percent_lbt_collisions = 0
    if number_ra_sensors > 0:
        percent_RA_collisions = np.sum(all_collision_array[np.where(dataframe['access_type'] ==1)[0]])/number_ra_sensors
    else: percent_RA_collisions = 0
    avg_backshift_time = backshift_time/sensors
    
    return [percent_backshift, percent_sensors_backshift, percent_allcollisions, percent_RA_collisions, percent_lbt_collisions, avg_backshift_time, dataframe]
  
all_backshifts = np.zeros((len(number_sensors),sim_repetitions))
number_shifted_sensors = np.zeros((len(number_sensors),sim_repetitions))
collision_array = np.zeros((len(number_sensors),sim_repetitions))
number_carryovers = np.zeros((len(number_sensors),sim_repetitions))
avg_shifted_time = np.zeros((len(number_sensors),sim_repetitions))

percent_backshift = np.zeros((len(number_sensors),len(percent_crosstraffic),sim_repetitions))
percent_sensors_backshift = np.zeros((len(number_sensors),len(percent_crosstraffic),sim_repetitions))
percent_allcollisions = np.zeros((len(number_sensors),len(percent_crosstraffic),sim_repetitions))
percent_RA_collisions = np.zeros((len(number_sensors),len(percent_crosstraffic),sim_repetitions))
percent_lbt_collisions = np.zeros((len(number_sensors),len(percent_crosstraffic),sim_repetitions))
avg_backshift_time = np.zeros((len(number_sensors),len(percent_crosstraffic),sim_repetitions))
 
for i in range(len(number_sensors)):
    print('i = ' + str(i/len(number_sensors)))
    #get maximal distance to x and y coordinates dependent on max distance from hata model; create more points than needed
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

    
    sensor_index = np.arange(number_sensors[i])+1
    
    for j in range(len(percent_crosstraffic)):
        print('j = ' + str(j/len(percent_crosstraffic)))
        lbt_sensors = np.zeros(int(number_sensors[i] - np.ceil(number_sensors[i] * percent_crosstraffic[j]/100)))
        ra_sensors = np.ones(int(np.ceil(number_sensors[i] * percent_crosstraffic[j]/100)))
        access_type_array = np.concatenate((lbt_sensors,ra_sensors), axis=0)
        
        carryover_dataframe = []
        for l in range(sim_repetitions): 
                    
            sensor_dataframe = pd.DataFrame({'index': sensor_index})
            sensor_dataframe['transmission_attempts'] = np.ones(int(number_sensors[i]))
            sensor_dataframe['access_type'] = access_type_array

            
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
               
        
            payload = np.random.randint(payload_max,size=int(number_sensors[i]))+payload_min
            sensor_dataframe['payload'] = payload
                
            #time on air calculation
            all_packet = (8 * sensor_dataframe['payload'] - (4*sensor_dataframe['spreading_factor']) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * sensor_dataframe['spreading_factor'] - 2*low_datarate_optimize)
            n_packet = 8 + (np.ceil(all_packet)* (coding_rate + 4))
            total_symbols = preamble_length + 4.25 + n_packet
            symbol_duration = (2**sensor_dataframe['spreading_factor'])/bandwidth
            sensor_dataframe['time_on_air'] = symbol_duration * total_symbols
            sensor_dataframe['transmission_starts'] = np.round(np.random.uniform(low = 0, high=3600, size=int(number_sensors[i])), number_accuracy)
            sensor_dataframe['transmission_ends'] = sensor_dataframe['transmission_starts'] + sensor_dataframe['time_on_air']
            sensor_dataframe['collisions'] = np.zeros(int(number_sensors[i]))
    
            sensor_dataframe = sensor_dataframe.append(carryover_dataframe)
    
            [percent_backshift[i][j][l], percent_sensors_backshift[i][j][l], percent_allcollisions[i][j][l], percent_RA_collisions[i][j][l], percent_lbt_collisions[i][j][l], avg_backshift_time[i][j][l], sensor_dataframe] = listen_before_talk(sensor_dataframe, int(number_sensors[i])) #full dataframe to function if all sensors use aloha
            carryover_dataframe = sensor_dataframe[sensor_dataframe['transmission_ends'] > 3600] 
            carryover_dataframe['transmission_starts'] = carryover_dataframe['transmission_starts'] - 3600
            carryover_dataframe['transmission_ends'] = carryover_dataframe['transmission_ends'] - 3600

        
    #%%

np.save('ra_lbt_percent_backshift_total_sfrecovery', percent_backshift)
np.save('ra_lbt_percent_sensors_backshift_sfrecovery', percent_sensors_backshift)
np.save('ra_lbt_percent_allcollisions_sfrecovery', percent_allcollisions)
np.save('ra_lbt_percent_RA_collisions_sfrecovery', percent_RA_collisions)
np.save('ra_lbt_percent_lbt_collisions_sfrecovery', percent_lbt_collisions)
np.save('ra_lbt_avg_backshift_time_sfrecovery', avg_backshift_time)




