# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:38:09 2023

@author: emide
"""

import sys
from wam_ipe_plotter import figure_save

command_arguments = sys.argv[1:]

for x in range(len(command_arguments)):
    filename = command_arguments[x]
    figure_save(filename)

