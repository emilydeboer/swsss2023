"""
Created on Tue Jul 25 11:42:36 2023

@author: emide
"""

__author__ = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

# dataset = nc.Dataset('\\Users\emide\Documents\swsss2023\day_02\wfs.t06z.20230725_05\wfs.t06z.ipe05.20230725_053000.nc')
                     
dir = '/Users/emide/Documents/swsss2023/day_02/' #folder for files
filename = 'omni_min_def_FokVF3TAiU.lst' 
# filename = 'omni_test.lst'
file_location = dir + filename


with open(file_location) as file:
        
    # instantiating variables
    year = []
    day = []
    hour = []
    minute = []
    symh = []
    times = []
    
    for line in file:
        temp = line.split() # putting each line in list
        year.append(int(temp[0])) # 1st index is year
        day.append(int(temp[1])) # 2nd index is day
        hour.append(int(temp[2])) # 3rd index is hour
        minute.append(int(temp[3])) # 4th index is minute
        symh.append(int(temp[4])) # 5th index is symh
        
        # setting the date correctly
        # Omni web has days as absolute (so 75 days = March 16th)
        # first part sets the date to Jan 1, then it adds the months, 
        # calculated with time delta
        datetime1 = dt.datetime(int(temp[0]), 1, 1, int(temp[2]), int(temp[3])) + dt.timedelta(days=int(temp[1])-1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        print(datetime1)
        times.append(datetime1) # puts dates into the list
       
        print(line)
        
plt.plot(times, symh, 'palevioletred') # PLOT
plt.xticks(rotation=45) # <-- makes the x axis diagonal
plt.xlabel('Time (UTC)') # labeling
plt.ylabel('SYM/H (nT)') #labeling
plt.title('Geomagnetic Storm on 3/17/2013') 
plt.grid()