#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 21:13:59 2021

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

all_collisions_no_recovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_no_recovery.npy') 
all_collisions_sf_recovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_sfrecovery.npy')
all_collisions_lesstraffic_no_recovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_lesstraffic_no_recovery.npy')
all_collisions_lesstraffic_largerslot_sfrecovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_lesstraffic_largerslots_sfrecovery.npy')
all_collisions_lesstraffic_sameslot_no_recovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_lesstraffic_sameslots_no_recovery.npy')
all_collisions_lesstraffic_sameslot_sfrecovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_lesstraffic_sameslots_sfrecovery.npy')
tmp_systematic_no_recovery_array = np.load('../results/slotted_randomAccess/all_systematic_collisions_array_array_no_recovery_location.npy')

#%%
#get all simruns with reconfigs
all_collisions_no_recovery = np.zeros((len(all_collisions_no_recovery_array[:,0,0,0]),len(all_collisions_no_recovery_array[0,:,0,0])))
all_collisions_sfrecovery = np.zeros((len(all_collisions_sf_recovery_array[:,0,0,0]),len(all_collisions_sf_recovery_array[0,:,0,0])))
all_collisions_lesstraffic_no_recovery = np.zeros((len(all_collisions_lesstraffic_no_recovery_array[:,0,0,0]),len(all_collisions_lesstraffic_no_recovery_array[0,:,0,0])))
all_collisions_lesstraffic_sfrecovery_ = np.zeros((len(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,0,0,0]),len(all_collisions_lesstraffic_largerslot_sfrecovery_array[0,:,0,0])))
all_collisions_lesstraffic_sameslot_no_recovery = np.zeros((len(all_collisions_lesstraffic_sameslot_no_recovery_array[:,0,0,0]),len(all_collisions_lesstraffic_sameslot_no_recovery_array[0,:,0,0])))
all_collisions_lesstraffic_sameslot_sfrecovery = np.zeros((len(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,0,0,0]),len(all_collisions_lesstraffic_sameslot_sfrecovery_array[0,:,0,0])))



#i: drift --> number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
percent_crosstraffic = [1,2,3,4,5,10,15,20,25,30,50]

#j: cross-traffic --> additional sensors percent_crosstraffic = [1,2,3,4,5,10,15,20,25,30,50]
for i in range(len(all_collisions_no_recovery_array[0,:,0,0])):
    for j in range(len(all_collisions_no_recovery_array[:,0,0,0])):
        all_collisions_no_recovery[i,j] = np.mean(all_collisions_no_recovery_array[i,j,:,:])
        all_collisions_sfrecovery[i,j] = np.mean(all_collisions_sf_recovery_array[i,j,:,:])
        all_collisions_lesstraffic_no_recovery[i,j] = np.mean(all_collisions_lesstraffic_no_recovery_array[i,j,:,:])
        all_collisions_lesstraffic_sfrecovery_[i,j] = np.mean(all_collisions_lesstraffic_largerslot_sfrecovery_array[i,j,:,:])
        all_collisions_lesstraffic_sameslot_no_recovery[i,j] = np.mean(all_collisions_lesstraffic_sameslot_no_recovery_array[i,j,:,:])
        all_collisions_lesstraffic_sameslot_sfrecovery[i,j] = np.mean(all_collisions_lesstraffic_sameslot_sfrecovery_array[i,j,:,:])

    
no_recovery_collision_data_crosstraffic = [np.ndarray.flatten(all_collisions_no_recovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_collisions_no_recovery_array[:,10,:,:])]

sfrecovery_collision_data_crosstraffic = [np.ndarray.flatten(all_collisions_sf_recovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_collisions_sf_recovery_array[:,10,:,:])]

no_recovery_lesstraffic_collision_data_crosstraffic = [np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[:,10,:,:])]

sfrecovery_lesstraffic_collision_data_crosstraffic = [np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[:,10,:,:])]

no_recovery_lesstraffic_sameslot_collision_data_crosstraffic = [np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[:,10,:,:])]

sfrecovery_lesstraffic_sameslot_collision_data_crosstraffic = [np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[:,10,:,:])]




no_recovery_collision_data_drift = [np.ndarray.flatten(all_collisions_no_recovery_array[0,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[1,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[2,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[3,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[4,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[5,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[6,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[7,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[8,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_no_recovery_array[9,:,:,:]),
                                    np.ndarray.flatten(all_collisions_no_recovery_array[10,:,:,:])]

sfrecovery_collision_data_drift = [np.ndarray.flatten(all_collisions_sf_recovery_array[0,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[1,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[2,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[3,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[4,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[5,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[6,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[7,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[8,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[9,:,:,:]),
                                    np.ndarray.flatten(all_collisions_sf_recovery_array[10,:,:,:])]

no_recovery_lesstraffic_collision_data_drift = [np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[0,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[1,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[2,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[3,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[4,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[5,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[6,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[7,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[8,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[9,:,:,:]),
                                    np.ndarray.flatten(all_collisions_lesstraffic_no_recovery_array[10,:,:,:])]

sfrecovery_lesstraffic_collision_data_drift = [np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[0,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[1,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[2,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[3,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[4,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[5,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[6,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[7,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[8,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[9,:,:,:]),
                                    np.ndarray.flatten(all_collisions_lesstraffic_largerslot_sfrecovery_array[10,:,:,:])]

no_recovery_lesstraffic_sameslot_collision_data_drift = [np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[0,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[1,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[2,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[3,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[4,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[5,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[6,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[7,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[8,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[9,:,:,:]),
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_no_recovery_array[10,:,:,:])]

sfrecovery_lesstraffic_sameslot_collision_data_drift = [np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[0,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[1,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[2,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[3,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[4,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[5,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[6,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[7,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[8,:,:,:]), 
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[9,:,:,:]),
                                    np.ndarray.flatten(all_collisions_lesstraffic_sameslot_sfrecovery_array[10,:,:,:])]

def grouped_boxplots(data_groups, ax=None, max_width=0.8, pad=0.05, **kwargs):
    if ax is None:
        ax = plt.gca()

    max_group_size = max(len(item) for item in data_groups)
    total_padding = pad * (max_group_size - 1)
    width = (max_width - total_padding) / max_group_size
    kwargs['widths'] = width

    def positions(group, i):
        span = width * len(group) + pad * (len(group) - 1)
        ends = (span - width) / 2
        x = np.linspace(-ends, ends, len(group))
        return x + i

    artists = []
    for i, group in enumerate(data_groups, start=1):
        artist = ax.boxplot(group, positions=positions(group, i), **kwargs)
        artists.append(artist)

    ax.margins(0.05)
    ax.set(xticks=np.arange(len(data_groups)) + 1)
    ax.autoscale()
    return artists


crosstraffic_data = [[no_recovery_collision_data_crosstraffic[0], no_recovery_lesstraffic_collision_data_crosstraffic[0], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[0]],
                     [no_recovery_collision_data_crosstraffic[1], no_recovery_lesstraffic_collision_data_crosstraffic[1], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[1]],
                     [no_recovery_collision_data_crosstraffic[2], no_recovery_lesstraffic_collision_data_crosstraffic[2], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[2]],
                     [no_recovery_collision_data_crosstraffic[3], no_recovery_lesstraffic_collision_data_crosstraffic[3], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[3]],
                     [no_recovery_collision_data_crosstraffic[4], no_recovery_lesstraffic_collision_data_crosstraffic[4], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[4]],
                     [no_recovery_collision_data_crosstraffic[5], no_recovery_lesstraffic_collision_data_crosstraffic[5], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[5]],
                     [no_recovery_collision_data_crosstraffic[6], no_recovery_lesstraffic_collision_data_crosstraffic[6], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[6]],
                     [no_recovery_collision_data_crosstraffic[7], no_recovery_lesstraffic_collision_data_crosstraffic[7], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[7]],
                     [no_recovery_collision_data_crosstraffic[8], no_recovery_lesstraffic_collision_data_crosstraffic[8], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[8]],
                     [no_recovery_collision_data_crosstraffic[9], no_recovery_lesstraffic_collision_data_crosstraffic[9], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[9]],
                     [no_recovery_collision_data_crosstraffic[10], no_recovery_lesstraffic_collision_data_crosstraffic[10], no_recovery_lesstraffic_sameslot_collision_data_crosstraffic[10]]]
  
drift_data = [[no_recovery_collision_data_drift[0], no_recovery_lesstraffic_collision_data_drift[0], no_recovery_lesstraffic_sameslot_collision_data_drift[0]],
                     [no_recovery_collision_data_drift[1], no_recovery_lesstraffic_collision_data_drift[1], no_recovery_lesstraffic_sameslot_collision_data_drift[1]],
                     [no_recovery_collision_data_drift[2], no_recovery_lesstraffic_collision_data_drift[2], no_recovery_lesstraffic_sameslot_collision_data_drift[2]],
                     [no_recovery_collision_data_drift[3], no_recovery_lesstraffic_collision_data_drift[3], no_recovery_lesstraffic_sameslot_collision_data_drift[3]],
                     [no_recovery_collision_data_drift[4], no_recovery_lesstraffic_collision_data_drift[4], no_recovery_lesstraffic_sameslot_collision_data_drift[4]],
                     [no_recovery_collision_data_drift[5], no_recovery_lesstraffic_collision_data_drift[5], no_recovery_lesstraffic_sameslot_collision_data_drift[5]],
                     [no_recovery_collision_data_drift[6], no_recovery_lesstraffic_collision_data_drift[6], no_recovery_lesstraffic_sameslot_collision_data_drift[6]],
                     [no_recovery_collision_data_drift[7], no_recovery_lesstraffic_collision_data_drift[7], no_recovery_lesstraffic_sameslot_collision_data_drift[7]],
                     [no_recovery_collision_data_drift[8], no_recovery_lesstraffic_collision_data_drift[8], no_recovery_lesstraffic_sameslot_collision_data_drift[8]],
                     [no_recovery_collision_data_drift[9], no_recovery_lesstraffic_collision_data_drift[9], no_recovery_lesstraffic_sameslot_collision_data_drift[9]],
                     [no_recovery_collision_data_drift[10], no_recovery_lesstraffic_collision_data_drift[10], no_recovery_lesstraffic_sameslot_collision_data_drift[10]]]
                              

#%%
n = 6
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1,figsize=(5, 3))
groups = grouped_boxplots(crosstraffic_data, max_width=0.9,
                          patch_artist=True, medianprops=dict(color='r'))

n=3
colors = plt.cm.copper(np.linspace(0,1,n))
for item in groups:
    for color, patch in zip(colors, item['boxes']):
        patch.set(facecolor=color)

proxy_artists = groups[-1]['boxes']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['1%', '2%', '3%', '4%', '5%', '10%', '15%', '20%', '25%', '30%', '50%'], rotation='vertical')
plt.legend(proxy_artists, ['S1.1', 'S1.2', 'S1.3'],
              loc='best')
plt.xlabel('Random access traffic [%]')
plt.ylabel('collision probability')
plt.gcf().subplots_adjust(bottom=0.25)
#plt.gcf().subplots_adjust(left=0.-0.05)
plt.savefig('../figures/slotted_crosstraffic_study.pdf')
#%%

plt.figure(2,figsize=(5, 3))
groups = grouped_boxplots(drift_data, max_width=0.9,
                          patch_artist=True, medianprops=dict(color='r'))

n=3
colors = plt.cm.copper(np.linspace(0,1,n))
for item in groups:
    for color, patch in zip(colors, item['boxes']):
        patch.set(facecolor=color)

proxy_artists = groups[-1]['boxes']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['2', '5', '10', '15', '20', '25', '50', '75', '100', '125', '150'], rotation='vertical')
plt.legend(proxy_artists, ['S1.1', 'S1.2', 'S1.3'],
              loc='best', ncol=3, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.xlabel('time drift [ppm]')
plt.ylabel('collision probability')
plt.gcf().subplots_adjust(bottom=0.25)
plt.savefig('../figures/slotted_time_drift_study.pdf')





