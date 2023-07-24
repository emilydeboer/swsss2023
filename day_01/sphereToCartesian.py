# -*- coding: utf-8 -*-
"""
A 3D plot script for spherical coordnates.
"""

__author__ = 'Emily DeBoer'
__email__ = 'edeboer@ucsd.edu'

import numpy as np
import matplotlib.pyplot as plt

def sphere_to_cart(r, theta, phi):
    """Changes spherical coordinates to cartesian coordinates. 
    theta = angle from x axis to projected vector on the x-y plane (radians)
    phi = angle from z axis to vector (radians)
    r = radius (can be any units)
    
    returns: x, y, z in the unit of radius
    """
    x = r*np.sin(phi)*np.cos(theta)
    y = r*np.sin(phi)*np.sin(theta)
    z = r*np.cos(phi)
    return x, y, z

test1 = sphere_to_cart(1, 0, 0)
test2 = sphere_to_cart(1, np.pi, np.pi)
test3 = sphere_to_cart(1, 2*np.pi, 2*np.pi)
test4 = sphere_to_cart(1, -np.pi/2, -2*np.pi)
test5 = sphere_to_cart(1, -2*np.pi, np.pi/2)

print(test1)
print(test2)
print(test3)
print(test4)
print(test5)
assert np.allclose(test1, (0, 0, 1), 1e-5), "Test 1 is not correct"
assert np.allclose(test2, (0, 0, -1), 1e-5), "Test 2 is not correct"
assert np.allclose(test3, (0, 0, 1), 1e-5), "Test 3 is not correct" 
assert np.allclose(test4, (0, 0, 1), 1e-5), "Test 4 is not correct" 
assert np.allclose(test5, (1, 0, 0), 1e-5), "Test 5 is not correct" 


fig = plt.figure()
axes = plt.axes(projection='3d')
r = np.linspace(0,1)
theta = np.linspace(0, 2*np.pi)
phi = np.linspace(0, 2*np.pi)
x, y, z = sphere_to_cart(r, theta, phi)
axes.plot(x,y,z)