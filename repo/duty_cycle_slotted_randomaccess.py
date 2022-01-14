#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 09:23:12 2021

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

all_sync = np.load('../results/slotted_randomAccess/all_syncs_array_no_recovery.npy')
all_sync_sf = np.load('../results/slotted_randomAccess/all_syncs_array_sfrecovery.npy')
all_sync_lesstraffic = np.load('../results/slotted_randomAccess/all_syncs_array_lesstraffic_no_recovery.npy')
all_sync_lesstrafficsf = np.load('../results/slotted_randomAccess/all_syncs_array_lesstraffic_largerslots_sfrecovery.npy')
all_sync_lesstraffic_sameslots = np.load('../results/slotted_randomAccess/all_syncs_array_lesstraffic_sameslots_no_recovery.npy')
all_sync_lesstraffic_sameslotssf = np.load('../results/slotted_randomAccess/all_syncs_array_lesstraffic_sameslots_sfrecovery.npy')

lost_sync = np.load('../results/slotted_randomAccess/all_synclosses_array_no_recovery.npy')
lost_sync_sf = np.load('../results/slotted_randomAccess/all_synclosses_array_sfrecovery.npy')
lost_sync_lesstraffic = np.load('../results/slotted_randomAccess/all_synclosses_array_lesstraffic_no_recovery.npy')
lost_sync_lesstrafficsf = np.load('../results/slotted_randomAccess/all_synclosses_array_lesstraffic_largerslots_sfrecovery.npy')
lost_sync_lesstraffic_sameslots = np.load('../results/slotted_randomAccess/all_synclosses_array_lesstraffic_sameslots_no_recovery.npy')
lost_sync_lesstraffic_sameslotssf = np.load('../results/slotted_randomAccess/all_synclosses_array_lesstraffic_sameslots_sfrecovery.npy')

s1_sync = np.zeros((len(all_sync[:,0,0,0]),len(all_sync[0,:,0,0])))
s1_syncsf = np.zeros((len(all_sync_sf[:,0,0,0]),len(all_sync_sf[0,:,0,0])))
s2_sync = np.zeros((len(all_sync_lesstraffic[:,0,0,0]),len(all_sync_lesstraffic[0,:,0,0])))
s2_syncsf = np.zeros((len(all_sync_lesstrafficsf[:,0,0,0]),len(all_sync_lesstrafficsf[0,:,0,0])))
s3_sync = np.zeros((len(all_sync_lesstraffic_sameslots[:,0,0,0]),len(all_sync_lesstraffic_sameslots[0,:,0,0])))
s3_syncsf = np.zeros((len(all_sync_lesstraffic_sameslotssf[:,0,0,0]),len(all_sync_lesstraffic_sameslotssf[0,:,0,0])))

#i: drift --> number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
percent_crosstraffic = [1,2,3,4,5,10,15,20,25,30,50]
ppm_drift = np.asarray([2,5,10,15,20,25,50,75,100,125,150])
for i in range(len(number_sensors)):
    current_slotted_messages = number_sensors[i]
    #current_crosstraffic = math.ceil(number_sensors[i] * percent_crosstraffic[l]/100)
    #all_messages = current_slotted_messages + current_crosstraffic
    for j in range(len(percent_crosstraffic)):
        s1_sync[i][j] = (np.mean(all_sync[i,j,:,:]) + np.mean(lost_sync[i,j,:,:])) * current_slotted_messages / 38.88965707964602
        s1_syncsf[i][j] = (np.mean(all_sync_sf[i,j,:,:]) + np.mean(lost_sync_sf[i,j,:,:])) * current_slotted_messages / 38.88965707964602

for i in range(len(number_sensors)):
    for j in range(len(percent_crosstraffic)):
        current_crosstraffic = math.ceil(number_sensors[i] * percent_crosstraffic[j]/100)
        all_messages = number_sensors[i]
        current_slotted_messages = all_messages - current_crosstraffic
        
        s2_sync[i][j] = (np.mean(all_sync_lesstraffic[i,j,:,:]) + np.mean(lost_sync_lesstraffic[i,j,:,:])) * current_slotted_messages / 38.88965707964602
        s2_syncsf[i][j] = (np.mean(all_sync_lesstrafficsf[i,j,:,:]) + np.mean(lost_sync_lesstraffic[i,j,:,:])) * current_slotted_messages / 38.88965707964602

        s3_sync[i][j] = (np.mean(all_sync_lesstraffic_sameslots[i,j,:,:]) + np.mean(lost_sync_lesstraffic_sameslots[i,j,:,:])) * current_slotted_messages / 38.88965707964602
        s3_syncsf[i][j] = (np.mean(all_sync_lesstraffic_sameslotssf[i,j,:,:]) + np.mean(lost_sync_lesstraffic_sameslotssf[i,j,:,:])) * current_slotted_messages / 38.88965707964602


        