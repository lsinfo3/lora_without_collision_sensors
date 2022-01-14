#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 17:58:07 2021

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

backoff_normal_1000 = pd.read_csv('../results/backoff_calc/backoff_normal_1000sensors.csv') #x
backoff_random_1000 = pd.read_csv('../results/backoff_calc/backoff_random_1000sensors.csv')
#backoff_short_random_1000 = pd.read_csv('../results/backoff_calc/backoff_random_smallrange_1000sensors.csv')

backoff_normal_1000_allshifts = (backoff_normal_1000['run1'] + backoff_normal_1000['run2'] + backoff_normal_1000['run3'] + backoff_normal_1000['run4'] + backoff_normal_1000['run5'])/5
backoff_random_1000_allshifts = (backoff_random_1000['run1'] + backoff_random_1000['run2'] + backoff_random_1000['run3'] + backoff_random_1000['run4'] + backoff_random_1000['run5'])/5
backoff_normal_1000_sensorshifts = (backoff_normal_1000['number_sensors_shifted1'] + backoff_normal_1000['number_sensors_shifted2'] + backoff_normal_1000['number_sensors_shifted3'] + backoff_normal_1000['number_sensors_shifted4'] + backoff_normal_1000['number_sensors_shifted5'])/5
backoff_random_1000_sensorshifts = (backoff_random_1000['number_sensors_shifted1'] + backoff_random_1000['number_sensors_shifted2'] + backoff_random_1000['number_sensors_shifted3'] + backoff_random_1000['number_sensors_shifted4'] + backoff_random_1000['number_sensors_shifted5'])/5

#backoff_short_random_1000_allshifts = (backoff_short_random_1000['run1'] + backoff_short_random_1000['run2'] + backoff_short_random_1000['run3'] + backoff_short_random_1000['run4'] + backoff_short_random_1000['run5'])/5
#backoff_short_random_1000_sensorshifts = (backoff_short_random_1000['number_sensors_shifted1'] + backoff_short_random_1000['number_sensors_shifted2'] + backoff_short_random_1000['number_sensors_shifted3'] + backoff_short_random_1000['number_sensors_shifted4'] + backoff_short_random_1000['number_sensors_shifted5'])/5


duration_normal_1000 = np.zeros(len(backoff_normal_1000_allshifts))

#backoff_short_random_1000_duration = backoff_short_random_1000['backoffs']

all_backoffs = backoff_normal_1000['backoffs']
duration_random_1000 = backoff_random_1000_allshifts * np.mean(all_backoffs)


for i in range(len(backoff_normal_1000_allshifts)):
    duration_normal_1000[i] = backoff_normal_1000_allshifts[i] * all_backoffs[i]
#%%
n = 6
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

fig = plt.figure(1, figsize=(5, 3))
ax = fig.add_subplot(111)
ax2 = ax.twinx()

p1, = ax.plot(all_backoffs, backoff_normal_1000_allshifts/1000, color=colors[2], linewidth = 2, label='number delays: delay by ToA')
p2, = ax2.plot(all_backoffs, duration_normal_1000/1000, color=colors[4], linewidth = 2, label='delay time: delay by ToA')
p3, = ax.plot(all_backoffs, (np.zeros(len(all_backoffs)) + np.mean(backoff_random_1000_allshifts/1000)), color=colors[0], linewidth = 2, label='number delays: random delay')
p4, = ax2.plot(all_backoffs, (np.zeros(len(all_backoffs)) + np.mean(duration_random_1000/1000)), color=colors[0], linewidth = 2, linestyle='--', label='delay time: random delay')


ax.set_xlabel('back-off delay [s]')
ax.set_ylabel('avg. delays per message')
ax.set_ylim(-0.07898880000000003,1.2)


ax2.set_ylabel('avg. delay time per message [s]')
ax2.set_ylim(-0.07898880000000003,1.2)

legend_handler = [p1,p2,p3,p4]

ax.legend(handles=legend_handler, loc='best', ncol=1, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, fontsize = 10)

ax.grid(which='major')
plt.gcf().subplots_adjust(bottom=0.18)
plt.gcf().subplots_adjust(left=0.14)
plt.gcf().subplots_adjust(right=0.86)
#plt.savefig('../figures/backoff_analysis.pdf')

