# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 14:21:35 2023

@author: Emily DeBoer
email: edeboer@ucsd.edu
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from swmfpy.web import get_omni_data

start_time = dt.datetime(2002, 4, 3) # my birthday!
end_time = dt.datetime(2002, 4, 4) # day after birthday
data = get_omni_data(start_time, end_time) # returns dictionary

for key in data.keys(): # printing to see what keys there are in dictionary
    print(key)
    
# print(np.shape(data['times'])) 
# print(np.shape(data['al'])) 

# checking to make sure AL and times the same size
if np.shape(data['times']) == np.shape(data['al']): 
    plt.plot(data['times'],data['al']) # plotting
    plt.ylabel('Magnitude of AL') # y axis title
    plt.xlabel('Date and Time ')   # x axis title
    plt.xticks(rotation=45) # <-- makes the x axis diagonal
    

min_index = np.argmin(data['al'])
print(min_index)

print(data['times'][min_index])
