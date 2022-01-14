import os
import pandas as pd
import numpy
import sys
import random
import math
import matplotlib.pyplot as plt
from datetime import datetime
from multiprocessing import Pool


# Examples:
# print(df.iloc[0]['start']) prints the column start at row 0
# print(payload_size_to_time(64,7,0)) returns the payload in ms for a payload of 64 bytes with sf 7


def payload_size_to_time(payload, sf):
    # data_rate_optimisation: BW 125kHz, SF>=11
    BW = 125
    PL = payload+3
    CR = 1
    CRC = 1
    H = 1
    DE = 0
    SF = sf
    npreamble = 8
    if(sf >= 11):
        DE = 1

    Rs = BW/(math.pow(2, SF))
    Ts = 1/(Rs)
    symbol = 8+max(math.ceil((8.0*PL-4.0*SF+28+16*CRC-20.0*H) /
                             (4.0*(SF-2.0*DE)))*(CR+4), 0)
    Tpreamble = (npreamble+4.25)*Ts
    Tpayload = symbol*Ts
    ToA = Tpreamble+Tpayload
    return ToA


def calculate_clock_drift(last_sync_time, current_time):
    time_drift_mode= random.randrange(101)
    if(time_drift_mode<50):
        m = 0.000081083333 #80ppm
        t = 5.4
    elif(time_drift_mode<90):
        m = 0.00006119496855 #60ppm
        t = 5.4
    else:
        m = 0.00002047558923 #20ppm
        t = 5.4

    current_time = current_time-last_sync_time
    return(m*current_time+t)


def generate_sensor_events(payload_bytes, sf,slot_length,guard_time):
    start = random.randrange(3600001)  # Start time
    #####Timeslot Calculations (Notes)#####
    x = start % (slot_length+2*guard_time)
    if(x != 0):
        start = start+((slot_length+2*guard_time)-x)+guard_time
    # payload_bytes=random.randrange(64)+1 #Payload size random
    # payload_bytes=8 #Payload size consistent
    #sync_error = random.randrange(2)-1
    sync_error = 0
    time_drift = sync_error+calculate_clock_drift(0, start)
    fin = start+payload_size_to_time(payload_bytes, sf)
    return({'start': float(start), 'fin': float(fin), 'sf': sf, 'bytes': int(payload_bytes), 'loss': 0, 'sync_error_ms': sync_error, 'time_drift_ms': time_drift})

def generate_sensor_events_continuation(orig_start_time,payload_bytes, sf,slot_length,guard_time):
    start = orig_start_time + 3600000
    #####Timeslot Calculations (Notes)#####
    x = start % (slot_length+2*guard_time)
    if(x != 0):
        start = start+((slot_length+2*guard_time)-x)+guard_time
    # payload_bytes=random.randrange(64)+1 #Payload size random
    # payload_bytes=8 #Payload size consistent
    #sync_error = random.randrange(2)-1
    sync_error = 0
    time_drift = sync_error+calculate_clock_drift(0, start)
    fin = start+payload_size_to_time(payload_bytes, sf)
    return({'start': float(start), 'fin': float(fin), 'sf': sf, 'bytes': int(payload_bytes), 'loss': 0, 'sync_error_ms': sync_error, 'time_drift_ms': time_drift})

def calculate_gateway_channel_use(gateway_channel_use,sf):
    return gateway_channel_use + payload_size_to_time(1,sf)

def run_sim(number_of_sensors, SF, payload_bytes, slot_length, guard_time):
    global max_acceptable_time_drift
    sim_hours=100
    timeonair=payload_size_to_time(payload_bytes,SF)
    starttimes=[random.randrange(3600001) for i in range(1,number_of_sensors)]
    lastsynctimes=[0 for i in range(1,number_of_sensors)]
    starttimes = sorted(starttimes)
    collision_probability=[0 for i in range(0,sim_hours)]
    number_of_time_sync_events=[0 for i in range(0,sim_hours)]
    for i in range(1,sim_hours):
        current_collisions=0
        current_transmissions=0
        for y in range(1,number_of_sensors-1):
            current_time=(i-1)*3600000+starttimes[y]
            if((starttimes[y-1]+timeonair+calculate_clock_drift(lastsynctimes[y-1],current_time))>starttimes[y]+calculate_clock_drift(lastsynctimes[y],current_time)):
                current_collisions+=1
                current_transmissions+=1
            else:
                current_transmissions+=1
            if(calculate_clock_drift(lastsynctimes[y],current_time)>max_acceptable_time_drift):
                number_of_time_sync_events[i]+=1
                current_transmissions+=1
                lastsynctimes[y]=current_time
        try:
            collision_probability[i]=current_collisions/current_transmissions
        except:
            collision_probability[i]=0
    return[collision_probability,number_of_time_sync_events]

if __name__ == '__main__':
    ##########Parameters##########
    number_of_sensors = 10000
    SF = 8
    payload_bytes = 200
    slot_length = payload_size_to_time(payload_bytes,SF)
    guard_time = 50 #ms
    gw_duty_cycle=0.01
    max_acceptable_time_drift=200 #ms
    ##########Run with device range##########
    #devices_against_collision = [0 for i in range(0, number_of_sensors)]
    #for i in range(0, number_of_sensors):
    #    if(i % (number_of_sensors/100) == 0):
    #        print(str(int((i/number_of_sensors)*100))+"%")
    #    devices_against_collision[i] = run_sim(
    #        i, SF, payload_bytes, slot_length, guard_time)

    #output = {"collisions": []}
    #for x in range(0, number_of_sensors):
    #    output['collisions'].append(devices_against_collision[x])
    #pd.DataFrame(data=output).to_csv('Sensors'+str(number_of_sensors)+' SF'+str(SF) +
    #                                 ' PL'+str(payload_bytes)+' SL'+str(int(slot_length))+' GT'+str(guard_time)+'.csv')
    #pd.DataFrame(data=output).to_json('Sensors'+str(number_of_sensors)+' SF'+str(SF) +
    #                                  ' PL'+str(payload_bytes)+' SL'+str(int(slot_length))+' GT'+str(guard_time)+'.json')
    results=run_sim(number_of_sensors, SF, payload_bytes, slot_length, guard_time)
    plt.plot(results[0])
    plt.xlabel('Sim Hours')
    plt.ylabel('collision probability')
    #plt.xscale("log")
    #plt.axis([1, number_of_sensors, 0, 1])
    plt.show()
