# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 13:36:06 2023

@author: emide
"""

__author__  = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

def plot_tec(dataset, figsize = (12,6)):
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = figsize)
    
    latitude = dataset['lat'] # x coords
    longitude = dataset['lon'] # y coords
    
    tec = dataset['tec'] # specificed dataset value
    
    fig, ax = plt.subplots(figsize=figsize) # instantiating figure + axes
    cs = plt.pcolormesh(longitude, latitude, tec) # color plot
    
    # labels + colorbar
    ax.set_title('Total Electron Count', fontsize = 16)
    ax.set_xlabel('Longitude', fontsize = 16)
    ax.set_ylabel('Latitude', fontsize = 16)
    cbar = fig.colorbar(cs, label = 'TECu')
    
    return fig, ax

def plot_selectdata(dataset, select_data, figsize = (12,6)):
    
    latitude = dataset['lat'] # x coords
    longitude = dataset['lon'] # y coords
    
    select_array = dataset[select_data] # specificed dataset value
    
    fig, ax = plt.subplots(figsize=figsize) # instantiating figure + axes
    cs = plt.pcolormesh(longitude, latitude, select_array, cmap = 'plasma') # color plot
    
    # labels + colorbar
    ax.set_title('Measured ' + select_data + ' Data', fontsize = 16)
    ax.set_xlabel('Longitude', fontsize = 16)
    ax.set_ylabel('Latitude', fontsize = 16)
    # print(dataset[select_type].units)
    cbar = fig.colorbar(cs, label = dataset[select_data].units)
    
    return fig, ax

def figure_save(dataset, select_data, infilename):
    
    plot_selectdata(dataset, select_data)
    
    outfilename = infilename + '.png'
    plt.savefig(outfilename)
    
    return


dataset = nc.Dataset('\\Users\emide\Downloads\wfs.t06z.20230725_05\wfs.t06z.ipe05.20230725_052500.nc')
select_data = 'HmF2'

print(dataset)

# plot_selectdata(dataset, select_data)
figure_save(dataset, select_data, 'hmf2 data test')