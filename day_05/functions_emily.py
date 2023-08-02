# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 11:31:39 2023

@author: emide
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
from swmfpy.web import get_omni_data
import pandas as pd

def downloadsdata(start_date, end_date):
    # written by Emily
    
    # downloads data
    data = get_omni_data(start_date, end_date) # returns dictionary

    return data

def selectweek(data, week_number):
    # written by Emily
    
    # grabbing the year from the first timestamp
    firsttime = data['times'][1] 
    year = firsttime.year 
    
    # instantiating start and end time in datetime format
    starttime = dt.datetime.fromisocalendar(year, week_number, 1)
    endtime = dt.datetime.fromisocalendar(year, week_number, 7)
    
    # making sure doesn't grab from before we have data (starts on Jan 1st for week 1)
    if week_number == 1:
        starttime = dt.datetime(year, 1, 1)

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
    
    print(timestamp)   
    print(len(timestamp))
    print(len(symhstamp))
    print(len(alstamp))

    return data_newdictionary, starttime, endtime
