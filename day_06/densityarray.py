# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:20:54 2023

@author: emide
"""

__author__ = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import matplotlib.pyplot as plt


def density_array(m_AMU = 28, n0 = 1e19,  nPts = 100):
    # constants
    m = np.ones(nPts)*m_AMU*1.67e-27 # kg
    k = np.ones(nPts)*1.38e-23

    # altitude array
    alt0 = 100 # km
    altN = 500 # km
    alt_array = np.arange(alt0, altN, (altN-alt0)/nPts) # km
    dz = (alt_array[1:] - alt_array[:-1])*1000
    dz = np.append(dz, dz[-1]) # m

    # radius and gravity array
    R = 6370 # km
    R_array = np.ones(nPts)*R # km
    g_array = 3.99e14/((R_array + alt_array)*1000)**2

    # temperature array
    T0 = 200
    TN = 1000
    T_array = np.arange(T0, TN, (TN - T0)/nPts)
    
    # H array
    H_array = k*T_array/(m*g_array)
                 
    # density array
    n_array = np.zeros(nPts)
    n_array[0] = n0
    
    for pt in range(1, nPts):
        n_array[pt] = T_array[pt-1]/T_array[pt]*n_array[pt-1]*np.exp(-dz[pt]/H_array[pt-1])
    
    print(n_array)
    
    return n_array, alt_array


N2_array, alt_array = density_array()
O2_array, alt_array = density_array(32, 0.3e19)
O_array, alt_array = density_array(16, 1e18)
fig = plt.figure(figsize = (10,15))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

ax1.plot(N2_array, alt_array, label = 'N2')
ax1.plot(O2_array, alt_array, label = 'O2')
ax1.plot(O_array, alt_array, label = 'O')
ax1.set_xlabel('Density')
ax1.set_ylabel('Altitude (km)')
ax1.legend()

ax2.plot(N2_array, alt_array, label = 'N2')
ax2.plot(O2_array, alt_array, label = 'O2')
ax2.plot(O_array, alt_array, label = 'O')
ax2.set_xscale("log")
ax2.legend()

ax2.set_xlabel('Linearized Density (ln(n))')
ax2.set_ylabel('Altitude (km)')