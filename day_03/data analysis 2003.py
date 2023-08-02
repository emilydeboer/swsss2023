# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:08:50 2023

@author: emide

how many storms went below -100 in 2003?
"""

__author__ = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

def read_ascii_file(filename,index, margin):
    ''' reading an ascii file
    INPUT
        filename: directory + filename of file (string)
        index: column where the data is
        margin: 
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
     
            # setting the date correctly
            # Omni web has days as absolute (so 75 days = March 16th)
            # first part sets the date to Jan 1, then it adds the months, 
            # calculated with time delta
            datetime1 = dt.datetime(int(temp[0]), 1, 1, int(temp[2]), int(temp[3])) + dt.timedelta(days=int(temp[1])-1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
            times.append(datetime1) # puts dates into the list
            
        # original data WITHOUT filter
        original_diction = {'times': times, 'data': data}
        
        time_array = np.array(original_diction['times']) # time into an array
        data_array = np.array(original_diction['data']) # data into an array
        mask_below_margin = (data_array <= margin) # boolean array for below margin
        mask_at_margin = (data_array == margin) # boolean array at margin
        print(mask_at_margin)
        print(sum(mask_at_margin))
        
        # storm start and end is when it passes margin and then comes back up again
        # this is the sum of all the marginal elements divided by two
        time_select = time_array[mask_below_margin] # times under margin
        data_select = data_array[mask_below_margin] # data under margin

        count_of_storms = 1
        
        index_start = []
        index_end = []
        loop = 0
        
        print('time array length', time_array.shape)
        print('Mask below margin length', len(mask_below_margin))
        print('time_array length', len(time_array))
        for i in range(len(mask_below_margin)-1): 
            loop = loop + 1
            if mask_below_margin[i] == False and mask_below_margin[i+1] == True:
                index_start.append(i) # getting all the start times of storms
            if mask_below_margin[i] == True and mask_below_margin[i+1] == False:
                index_end.append(i) # this is going to get all the end times of storms
        
        # print('index length', len(index_start))
        # print(' number of loops', loop)
        print(' start index length', len(index_start))
        print(' end index length', len(index_end))
        # print(time_array[87424])
       
        hours = 12
        delta = dt.timedelta(0, 0, 0, 0, 0, hours)
        
        for x in range(len(index_start)-2):
            # print(x)
            # print(index_end[x])
            
            print('end   ',time_array[index_end[x]])
            print('start ', time_array[index_start[x+1]])
            if time_array[index_end[x]] < (time_array[index_start[x+1]]-delta):
                # print('end   ',time_array[index_end[x]])
                # print('start ', time_array[index_start[x+1]])

                count_of_storms = count_of_storms + 1
                
        # print('15 end   ',time_array[index_end[15]])
        # print('15 start ', time_array[index_start[15+1]])
        # print('16 end   ',time_array[index_end[16]])
        # print('16 start ', time_array[index_start[16+1]])

        # dictionary with both select time and data        
        select_diction = {'times': time_select, 'data': data_select}
            
    return original_diction, select_diction, count_of_storms

# only will run if in main body of code
if __name__ == "__main__":

    dir = '/Users/emide/Documents/swsss2023/day_03/' #folder for files
    filename =  dir + 'omni_5min_def_8ugF4pxEzY.lst' # file name
    index = -1 # data column
    margin = -100 # threshold
    
    original, select, count = read_ascii_file(filename,index, margin) # call function
    
    
    plt.plot(original['times'], original['data'], 'cadetblue') # plot all data
    plt.plot(select['times'], select['data'], 'red') # plot storm data
    plt.xticks(rotation=45) # <-- makes the x axis diagonal
    plt.xlabel('Time (UTC)') # labeling
    plt.ylabel('SYM/H (nT)') #labeling
    plt.title('Geomagnetic Storms in 2003') 

    # print number of storm data
    print('Number of Storms below', margin, 'with 12 hours between them:', count)
    # print('Number of storms that occured below -100 SYM/H:', int(count))
