# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:29:18 2023

@author: emide
"""

__author__ = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def read_ascii_file(filename,index, starttime, endtime):
    ''' reading an ascii file
    INPUT
        filename: directory + filename of file (string)
        index: column where the data is
    OUTPUT
        a dictionary with two key terms "times" and "data"
    
    '''

    with open(filename) as file:
            
        # instantiating variables
        year = []
        day = []
        hour = []
        minute = []
        data = []
        times = []
        
        for line in file:
            temp = line.split() # putting each line in list
            year.append(int(temp[0])) # 1st index is year
            day.append(int(temp[1])) # 2nd index is day
            hour.append(int(temp[2])) # 3rd index is hour
            minute.append(int(temp[3])) # 4th index is minute
            data.append(float(temp[index])) # index of data
     
            print(line)
   
            datetime1 = dt.datetime(int(temp[0]), 1, 1, int(temp[2]), int(temp[3])) + dt.timedelta(days=int(temp[1])-1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
            print(datetime1)
            times.append(datetime1) # puts dates into the list
            
        original_diction = {'times': times, 'data': data}
        
        time_array = np.array(original_diction['times'])
        data_array = np.array(original_diction['data'])
        mask = (time_array > starttime) & (time_array < endtime)
        time_select = time_array[mask]
        data_select = data_array[mask]

        select_diction = {'times': time_select, 'data': data_select}
            
    return original_diction, select_diction

if __name__ == "__main__":

    dir = '/Users/emide/Documents/swsss2023/day_02/' #folder for files
    filename =  dir + 'omni_min_def_FokVF3TAiU.lst'
    index = -1
    starttime = dt.datetime(2013, 3, 17)
    endtime = dt.datetime(2013, 3, 19)
    
    original, select = read_ascii_file(filename,index, starttime, endtime)
    
    
    plt.plot(original['times'], original['data'], 'cadetblue') # PLOT all data
    plt.plot(select['times'], select['data'], 'red') # PLOT storm data
    plt.xticks(rotation=45) # <-- makes the x axis diagonal
    plt.xlabel('Time (UTC)') # labeling
    plt.ylabel('SYM/H (nT)') #labeling
    plt.title('Geomagnetic Storm on 3/17/2013') 

# below 100