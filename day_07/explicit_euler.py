# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:30:13 2023

@author: emide
"""

import numpy as np
import matplotlib.pyplot as plt

h = 0.01
x_array = [3]

times = np.arange(0, 2, h)

for t in range(1, len(times)):
    x_in = x_array[t-1]
    x_array.append(x_in + h*(-2*x_in))
    
    
plt.plot(times, x_array, label = 'Explicit Euler', linestyle = 'dashed')
plt.plot(times, 3*np.exp(-2*times), label = 'Analytical')
plt.legend()