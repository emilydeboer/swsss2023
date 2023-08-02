# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 09:22:07 2023

@author: emide
"""

# Project 3

__author__ = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from swmfpy.web import get_omni_data
import pandas as pd


def downloadsdata(year):
    ''' This function downloads data from the year specified from the omniweb 
    database from python.
    Inputs:
        year: chosen time [format: integer]
    Outputs:
        data: all keys and data from omniweb for the specified year
        [format: dictionary]
    '''
    
    # written by Emily
    
    # downloads data
    start_time = dt.datetime(year, 1, 1)
    end_time = dt.datetime(year, 12, 31)
    data = get_omni_data(start_time, end_time) # returns dictionary

    return data

def selectweek(data, week_number):
    ''' This function returns cropped data according to week number. Week 
    number is specified starting from the beginning of the year. 
    Inputs:
        data: full data range of the year [format: dictionary]
        week_number: chosen week [format: integer]
    Outputs:
        data_newdictionary: cropped data only in the specified week
            relevant keys: times, al, sym_h [format: dictionary]
        week_number: chosen week [format: integer]  '''
    
    # written by Emily
    
    # grabbing the year from the first timestamp
    firsttime = data['times'][0] 
    year = firsttime.year 
    
    # instantiating start and end time in datetime format
    starttime = dt.datetime.fromisocalendar(year, week_number, 1)
    endtime = dt.datetime.fromisocalendar(year, week_number, 7)
    
    # making sure doesn't grab from before we have data (starts on Jan 1st for week 1)
    if week_number == 1:
        starttime = dt.datetime(year, 1, 1)
        
    if week_number == 52:
        endtime =  dt.datetime(year, 12, 31)

    # new variables within start and end time
    timestamp = []
    symhstamp = []
    alstamp = []
        
    times_array = np.array(data['times'])
    symh_array = np.array(data['sym_h'])
    al_array = np.array(data['al'])
    
    for n in range(len(times_array)):
        if starttime <= times_array[n] <= endtime:
            timestamp.append(times_array[n])
            symhstamp.append(symh_array[n])
            alstamp.append(al_array)
    
    # new dictionary data -- SAME keys
    data_newdictionary = {'times': timestamp, 'sym_h': symhstamp, 'al': alstamp}

    return data_newdictionary, week_number


def countstorm(data, threshold = -100):
    ''' This function returns cropped data according to week number. Week 
    number is specified starting from the beginning of the year. 
    Inputs:
        data: chosen data to count storms [format: dictionary]
        threshold: sym_h threshold, default = -100 [format: integer]
    Outputs:
        count_of_storms: number of storms with 12 hrs btw them
        [format: integer] 
        start_time: start time of storms after the 12 hrs condition [format: datetime]
        end_time: end time of storms after the 12 hrs condition[format: datetime]'''
    
    # written by Emily
    
    time_array = np.array(data['times']) # time into array
    symh_array = np.array(data['sym_h']) # symh into array
    mask = (symh_array <= threshold) # boolean array for below margin
        
    # storm start and end is when it passes margin and then comes back up again
    # this is the sum of all the marginal elements divided by two
    time_select = time_array[mask] # times under margin
    symh_select = symh_array[mask] # data under margin
        
    index_start = []
    index_end = []
            
    # loop tofind index of start and end time of storm
    for i in range(len(mask)-1): 
        if mask[i] == False and mask[i+1] == True:
            index_start.append(i) # getting all the start times of storms
        if mask[i] == True and mask[i+1] == False:
            index_end.append(i) # this is going to get all the end times of storms
           
    hours = 12
    delta = dt.timedelta(0, 0, 0, 0, 0, hours)
        
    # loop to count storm ONLY IF the end/start time are 12 hrs apart
    if (mask == True).any():
        count_of_storms = 1
        
        index_start_final = [index_start[0]]    
        index_end_final = []
        
        for x in range(len(index_start)-2):
            if time_array[index_end[x]] < (time_array[index_start[x+1]]-delta):
                count_of_storms = count_of_storms + 1
                index_start_final.append(index_start[x+1])
                index_end_final.append(index_end[x])
                
        index_end_final.append(index_end[-1])
        
        print(len(index_end_final))
        print(len(index_start_final))
        
        start_time = [time_array[i] for i in index_start_final]
        end_time = [time_array[i] for i in index_end_final]
        print(start_time)
        print(end_time)

    else:
        count_of_storms = 0
        start_time = []
        end_time = []
    
    # dictionary with both select time and data        
    select_diction = {'times': time_select, 'sym_h': symh_select}
    
    print('Number of Storms with 12 hours between them:', count_of_storms)
    
    # add index of start and end of each storm
    return count_of_storms, start_time, end_time


# if __name__ == "__main__":
#     start_time = dt.datetime(2013, 1, 1)
#     end_time = dt.datetime(2013, 12, 31)
#     week_start = dt.datetime(2013, 5, 3)
#     margin = -100
    
#     data = downloadsdata(start_time, end_time)
#     data_dict, number = selectweek(data, 1)
#     number = countstorm(data_dict)
    
