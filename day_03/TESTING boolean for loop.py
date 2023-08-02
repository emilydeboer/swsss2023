# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:59:27 2023

@author: emide
"""

# test code

mask = [False, False, False, True, True, False, False]


for i in range(0,len(mask)):
        if mask[i] == True and mask[i+1] == False:
            print("yes")