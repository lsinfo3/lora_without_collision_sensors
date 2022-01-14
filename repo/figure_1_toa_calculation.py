#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 17:29:30 2021

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

payload = np.arange(51) + 1
sf = np.arange(6)+7

toa_sf7 = np.zeros(len(payload))
toa_sf8 = np.zeros(len(payload))
toa_sf9 = np.zeros(len(payload))
toa_sf10 = np.zeros(len(payload))
toa_sf11 = np.zeros(len(payload))
toa_sf12 = np.zeros(len(payload))

toas = [toa_sf7, toa_sf8, toa_sf9, toa_sf10, toa_sf11, toa_sf12]

#lora related parameters
payload_bytes = 1
cyclic_redundancy_check = 1
header_enabled = 1
header_length = 20
low_datarate_optimize = 0
coding_rate = 4
preamble_length = 8
bandwidth = 125000

for i in range(len(sf)):
    all_packet = (8 * payload - (4*sf[i]) + 8 + 16 * cyclic_redundancy_check + 20 * header_enabled) / (4 * sf[i] - 2*low_datarate_optimize)
    n_packet = 8 + np.ceil(all_packet)* (coding_rate + 4)
    total_symbols = preamble_length + 4.25 + n_packet
    symbol_duration = (2**sf[i])/bandwidth
    toas[i] = symbol_duration * total_symbols

n = 8
colors = plt.cm.copper(np.linspace(0,1,n))
plt.rcParams.update({'font.size': 12})

plt.figure(1, figsize=(5, 3))

plt.plot(payload, toas[0], color=colors[0], linewidth = 2, label='SF7')
plt.plot(payload, toas[1], color=colors[0], linewidth = 2, linestyle='dashed', label='SF8')
plt.plot(payload, toas[2], color=colors[4], linewidth = 2, label='SF9')
plt.plot(payload, toas[3], color=colors[4], linewidth = 2, linestyle='dashed', label='SF10')
plt.plot(payload, toas[4], color=colors[6], linewidth = 2, label='SF11')
plt.plot(payload, toas[5], color=colors[6], linewidth = 2, linestyle='dashed', label='SF12')

#plt.plot(np.sort(error_noKnownVideos), yaxis_unknown, color=colors[13])
#plt.plot(np.sort(meanError), yaxis_unknown, color=colors[18])

#plt.arrow(48, 0, -20, 2.3, color='black', head_length = 0.5, head_width = 0.1, linewidth = 2, length_includes_head = False)


plt.ylabel('time on air [s]')
plt.xlabel('payload [B]')
#plt.xlim(-0.1, 4)
plt.grid(which='major')
tmp = plt.legend(loc="best", ncol=2, labelspacing = 0.2, borderaxespad = 0.4, columnspacing = 1.2, handlelength = 1.2)
plt.gcf().subplots_adjust(bottom=0.18)
plt.savefig('../figures/toa_analysis.pdf')


