#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 10:41:00 2021

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

all_crosstraffic_collisions_no_recovery_array = np.load('../results/slotted_randomAccess/all_collisions_array_no_recovery_location.npy')

#get all simruns with reconfigs
all_crosstraffic_collisions_no_recovery = np.zeros((len(all_crosstraffic_collisions_no_recovery_array[:,0,0,0]),len(all_crosstraffic_collisions_no_recovery_array[0,:,0,0])))


all_collisions_no_recovery_array = np.load('../results/slotted_lbt_study/all_collisions_slotted_lbt_no_recovery.npy')

#get all simruns with reconfigs
all_collisions_no_recovery = np.zeros((len(all_collisions_no_recovery_array[:,0,0,0]),len(all_collisions_no_recovery_array[0,:,0,0])))



#i: drift --> number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
number_sensors = [873,826,765,718,679,647,540,475,430,396,370]
percent_crosstraffic = [1,2,3,4,5,10,15,20,25,30,50]

#j: cross-traffic --> additional sensors percent_crosstraffic = [1,2,3,4,5,10,15,20,25,30,50]
for i in range(len(all_collisions_no_recovery_array[0,:,0,0])):
    for j in range(len(all_collisions_no_recovery_array[:,0,0,0])):
        all_collisions_no_recovery[i,j] = np.mean(all_collisions_no_recovery_array[i,j,:,:])

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

 
no_recovery_crosstraffic_collision_data_crosstraffic = [np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,0,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,1,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,2,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,3,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,4,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,5,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,6,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,7,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,8,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,9,:,:]), 
                                           np.ndarray.flatten(all_crosstraffic_collisions_no_recovery_array[:,10,:,:])]



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


crosstraffic_data_lbt= [[no_recovery_crosstraffic_collision_data_crosstraffic[0], no_recovery_collision_data_crosstraffic[0]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[1], no_recovery_collision_data_crosstraffic[1]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[2], no_recovery_collision_data_crosstraffic[2]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[3], no_recovery_collision_data_crosstraffic[3]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[4], no_recovery_collision_data_crosstraffic[4]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[5], no_recovery_collision_data_crosstraffic[5]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[6], no_recovery_collision_data_crosstraffic[6]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[7], no_recovery_collision_data_crosstraffic[7]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[8], no_recovery_collision_data_crosstraffic[8]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[9], no_recovery_collision_data_crosstraffic[9]],
                     [no_recovery_crosstraffic_collision_data_crosstraffic[10], no_recovery_collision_data_crosstraffic[10]]]



#%%
n = 6
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1,figsize=(5, 3))
groups = grouped_boxplots(crosstraffic_data_lbt, max_width=0.9,
                          patch_artist=True, medianprops=dict(color='r'))

n=3
colors = plt.cm.copper(np.linspace(0,1,n))
for item in groups:
    for color, patch in zip(colors, item['boxes']):
        patch.set(facecolor=color)

proxy_artists = groups[-1]['boxes']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], ['1%', '2%', '3%', '4%', '5%', '10%', '15%', '20%', '25%', '30%', '50%'], rotation='vertical')
plt.legend(proxy_artists, ['S1.1', 'S2.1'],
              loc='best')
plt.xlabel('other traffic [%]')
plt.ylabel('collision probability')
plt.gcf().subplots_adjust(bottom=0.25)
plt.gcf().subplots_adjust(left=0.15)
#plt.gcf().subplots_adjust(left=0.-0.05)
plt.savefig('../figures/slotted_lbt_ra_comparison.pdf')



