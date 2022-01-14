#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 20:43:40 2021

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

ra_lbt_avg_backshift_time = np.load('../results/ra_lbt_results/ra_lbt_avg_backshift_time.npy')
ra_lbt_percent_allcollisions = np.load('../results/ra_lbt_results/ra_lbt_percent_allcollisions.npy')
ra_lbt_percent_backshift_total = np.load('../results/ra_lbt_results/ra_lbt_percent_backshift_total.npy')
ra_lbt_percent_lbt_collisions = np.load('../results/ra_lbt_results/ra_lbt_percent_lbt_collisions.npy')
ra_lbt_percent_RA_collisions = np.load('../results/ra_lbt_results/ra_lbt_percent_RA_collisions.npy')
ra_lbt_percent_sensors_backshift = np.load('../results/ra_lbt_results/ra_lbt_percent_sensors_backshift.npy')

ra_lbt_avg_backshift_time_sfrecovery = np.load('../results/ra_lbt_sf/ra_lbt_avg_backshift_time_sfrecovery.npy')
ra_lbt_percent_allcollisions_sfrecovery = np.load('../results/ra_lbt_sf/ra_lbt_percent_allcollisions_sfrecovery.npy')
ra_lbt_percent_backshift_total_sfrecovery = np.load('../results/ra_lbt_sf/ra_lbt_percent_backshift_total_sfrecovery.npy')
ra_lbt_percent_lbt_collisions_sfrecovery = np.load('../results/ra_lbt_sf/ra_lbt_percent_lbt_collisions_sfrecovery.npy')
ra_lbt_percent_RA_collisions_sfrecovery = np.load('../results/ra_lbt_sf/ra_lbt_percent_RA_collisions_sfrecovery.npy')
ra_lbt_percent_sensors_backshift_sfrecovery = np.load('../results/ra_lbt_sf/ra_lbt_percent_sensors_backshift_sfrecovery.npy')

#%%
all_collisions_0_ra = np.zeros(77)
all_collisions_10_ra = np.zeros(77)
all_collisions_20_ra = np.zeros(77)
all_collisions_50_ra = np.zeros(77)
all_collisions_100_ra = np.zeros(77)
for i in range(len(ra_lbt_percent_allcollisions[:,0,0])):
    all_collisions_0_ra[i] = np.mean(ra_lbt_percent_allcollisions[i,0,:])
    all_collisions_10_ra[i] = np.mean(ra_lbt_percent_allcollisions[i,6,:])
    all_collisions_20_ra[i] = np.mean(ra_lbt_percent_allcollisions[i,8,:])
    all_collisions_50_ra[i] = np.mean(ra_lbt_percent_allcollisions[i,12,:])
    all_collisions_100_ra[i] = np.mean(ra_lbt_percent_allcollisions[i,22,:])
    
all_collisions_0_ra_sf = np.zeros(77)
all_collisions_10_ra_sf = np.zeros(77)
all_collisions_20_ra_sf = np.zeros(77)
all_collisions_50_ra_sf = np.zeros(77)
all_collisions_100_ra_sf = np.zeros(77)

lbt_only_avg_backshift_time = np.zeros(77)
lbt_only_backshift_total = np.zeros(77)
lbt_only_percent_sensors_backshift = np.zeros(77)

for i in range(len(ra_lbt_percent_allcollisions[:,0,0])):
    all_collisions_0_ra_sf[i] = np.mean(ra_lbt_percent_allcollisions_sfrecovery[i,0,:])
    all_collisions_10_ra_sf[i] = np.mean(ra_lbt_percent_allcollisions_sfrecovery[i,6,:])
    all_collisions_20_ra_sf[i] = np.mean(ra_lbt_percent_allcollisions_sfrecovery[i,8,:])
    all_collisions_50_ra_sf[i] = np.mean(ra_lbt_percent_allcollisions_sfrecovery[i,12,:])
    all_collisions_100_ra_sf[i] = np.mean(ra_lbt_percent_allcollisions_sfrecovery[i,22,:])
    lbt_only_avg_backshift_time[i] = np.mean(ra_lbt_avg_backshift_time[i,0,:])
    lbt_only_backshift_total[i] = np.mean(ra_lbt_percent_backshift_total[i,0,:])
    lbt_only_percent_sensors_backshift[i] = np.mean(ra_lbt_percent_sensors_backshift[i,0,:])
  
    
ra_lbt_avg_backshift_time1000 = np.zeros(23)
ra_lbt_avg_backshift_time1000_sf = np.zeros(23)
ra_lbt_backshift_total1000 = np.zeros(23)
ra_lbt_backshift_total1000_sf = np.zeros(23)
ra_lbt_percent_sensors_backshift1000 = np.zeros(23)
ra_lbt_percent_sensors_backshift1000_sf = np.zeros(23)

for i in range(len(ra_lbt_percent_allcollisions[0,:,0])):
    ra_lbt_avg_backshift_time1000[i] = np.mean(ra_lbt_avg_backshift_time[36,i,:])
    ra_lbt_avg_backshift_time1000_sf[i] = np.mean(ra_lbt_avg_backshift_time_sfrecovery[36,i,:])
    ra_lbt_backshift_total1000[i] = np.mean(ra_lbt_percent_backshift_total[36,i,:])
    ra_lbt_backshift_total1000_sf[i] = np.mean(ra_lbt_percent_backshift_total_sfrecovery[36,i,:])
    ra_lbt_percent_sensors_backshift1000[i] = np.mean(ra_lbt_percent_sensors_backshift[36,i,:])
    ra_lbt_percent_sensors_backshift1000_sf[i] = np.mean(ra_lbt_percent_sensors_backshift_sfrecovery[36,i,:])

    
    
percent_crosstraffic = [0,1,2,3,5,10,15,20,25,30,40,50,60,70,75,80,85,90,95,97,98,99,100]
number_sensors = np.arange(77)*25+100
n = 5
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1,figsize=(5, 3))
plt.plot(number_sensors, all_collisions_0_ra,color=colors[0], linewidth = 2, label='0%')
plt.plot(number_sensors, all_collisions_10_ra,color=colors[1], linewidth = 2, label='10%')
plt.plot(number_sensors, all_collisions_20_ra,color=colors[2], linewidth = 2, label='20%')
plt.plot(number_sensors, all_collisions_50_ra,color=colors[3], linewidth = 2, label='50%')
plt.plot(number_sensors, all_collisions_100_ra, color=colors[4], linewidth = 2, label='100%') 

plt.plot(number_sensors, all_collisions_0_ra_sf,color=colors[0], linestyle='dashed',linewidth = 2)
plt.plot(number_sensors, all_collisions_10_ra_sf,color=colors[1], linestyle='dashed',linewidth = 2)
plt.plot(number_sensors, all_collisions_20_ra_sf,color=colors[2], linestyle='dashed',linewidth = 2)
plt.plot(number_sensors, all_collisions_50_ra_sf,color=colors[3], linestyle='dashed',linewidth = 2)
plt.plot(number_sensors, all_collisions_100_ra_sf, color=colors[4],linestyle='dashed', linewidth = 2)  

plt.grid(which='major')
plt.legend(loc='best', ncol=1, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.xlabel('number messages per hour')
plt.ylabel('collision probability')
plt.gcf().subplots_adjust(bottom=0.18)
#plt.gcf().subplots_adjust(left=0.15)
plt.savefig('../figures/lbt_ra_collision_by_number_messages.pdf')
 