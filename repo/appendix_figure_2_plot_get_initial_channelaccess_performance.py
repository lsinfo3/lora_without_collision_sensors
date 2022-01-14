#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 13:31:53 2021

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

#lowerSF is with location!
aloha_collision_sf = pd.read_csv('../results/single_channel_access_results/aloha_collisions_lowerSF.csv')
aloha_collision = pd.read_csv('../results/single_channel_access_results/aloha_collisions.csv')
#slotted_normal = pd.read_csv('../results/single_channel_access_results/slotted_messages.csv')
#slotted_avg = pd.read_csv('../results/single_channel_access_results/slotted_messages_avg.csv')
#slotted_avg_toa = pd.read_csv('../results/single_channel_access_results/slotted_messages_avg_toa.csv')
#lbt_no_location = pd.read_csv('../results/single_channel_access_results/lbt_backshift_by_sensornumber_nolocation.csv')
lbt_location = pd.read_csv('../results/single_channel_access_results/lbt_backshift_by_sensornumber_location.csv')

aloha_probability = aloha_collision['collision_probability']
aloha_probability_sf = aloha_collision_sf['collision_probability']
#ticks = aloha_collision['ticks']

ticks = np.linspace(0.005,0.25,1000)

aloha_messages_per_probab_sf = aloha_collision_sf['messages_per_colissionprobab']
aloha_messages_per_probab = aloha_collision['messages_per_colissionprobab']

aloha_ticks = aloha_collision['ticks']
aloha_ticks_sf = aloha_collision_sf['ticks']

lbt_location_collision_probab = np.zeros(np.size(lbt_location['collisions']))
lbt_shifts_probab = np.zeros(np.size(lbt_location['collisions']))

for i in range(np.size(lbt_location['collisions'])):
    lbt_location_collision_probab[i] = lbt_location['collisions'][i]/(i+1)
    lbt_shifts_probab[i] = lbt_location['number_sensors_shifted'][i]/(i+1)

ticks_sf = np.linspace(0.005,0.30,1000)
messages_per_probab_sf = np.zeros(len(ticks))
for i in range(len(ticks)):
    messages_per_probab_sf[i] = np.size(np.where(aloha_collision_sf['collision_probability'] <= ticks_sf[i]))

lbt_messages_per_probab_lost = np.zeros(len(ticks))
lbt_messages_per_probab_shifts= np.zeros(len(ticks))



for i in range(len(ticks)):
    lbt_messages_per_probab_lost[i] = np.size(np.where(lbt_location_collision_probab <= ticks[i]))
    lbt_messages_per_probab_shifts[i] = np.size(np.where(lbt_shifts_probab <= ticks[i]))

#%%    
n = 3
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1, figsize=(5, 3))


plt.plot(aloha_ticks, aloha_messages_per_probab, color=colors[0], linewidth = 2, label='RA 1 collided')
plt.plot(ticks_sf, messages_per_probab_sf, color=colors[0], linestyle='dashed', linewidth = 2, label='RA 2 collided')

plt.plot(ticks, lbt_messages_per_probab_lost, color=colors[1], linewidth = 2, label='LBT collided')
plt.plot(ticks[np.where(lbt_messages_per_probab_shifts<2500)], lbt_messages_per_probab_shifts[np.where(lbt_messages_per_probab_shifts<2500)], color=colors[2], linewidth = 2,  label='LBT delayed')
#p5, = ax2.plot(
plt.xlabel('Percentage packets collided or delayed')
plt.ylabel('Messages per hour')
plt.xlim(0, 0.22)
plt.ylim(0, 2400)
plt.grid(which='major')
tmp = plt.legend(loc="best", ncol=1, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.gcf().subplots_adjust(bottom=0.18)
plt.gcf().subplots_adjust(left=0.15)
plt.savefig('../figures/collision_probab_comparison.pdf')
        
        
        
    
