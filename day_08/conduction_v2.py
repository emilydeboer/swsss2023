#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from tridiagonal import solve_tridiagonal

# ----------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------

if __name__ == "__main__":

    dx = 0.25

    # set x with 1 ghost cell on both sides:
    x = np.arange(-dx, 10 + 2 * dx, dx)

    t_lower = 200.0
    t_upper = 1000.0

    nPts = len(x)

    # set default coefficients for the solver:
    a = np.zeros(nPts) - 1
    b = np.zeros(nPts) + 2
    c = np.zeros(nPts) - 1
    d = np.zeros(nPts)
    
    # additions
    lam = 10
    
    # time dependent term
    nDays = 3
    dt = 1
    times = np.arange(0, nDays*24, dt)
    lon = 0.0
    
    # instantiate figure
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(111)

    # temperature grid to store temps at different times
    temp_grid = np.zeros([len(times), len(x)])

    for i, hour in enumerate(times):
        ut = hour % 24
        local_time = lon/15 + ut
        
        factor = -np.cos(local_time/24*2*np.pi)
        if factor < 0:
            factor = 0
            
        sun_heat = 100
    
        # setting Q for only some altitudes
        cond = np.logical_and(x < 7, x > 3)
        
        QEUV = np.zeros(nPts)    
        QEUV[cond] = -sun_heat*factor
        
        Qback = np.zeros(nPts)
        Qback[cond] = -100
       
        Qtotal = Qback + QEUV
        
        # change in altitude and final d column for tridiagonal solver
        dz = x[1] - x[0]
        dz2 = dz*dz
        d[:] = -Qtotal*dz2/lam

        # boundary conditions (bottom - fixed):
        a[0] = 0
        b[0] = 1
        c[0] = 0
        d[0] = t_lower

        # top - fixed:
        a[-1] = 1
        b[-1] = -1
        c[-1] = 0
        d[-1] = 0
    
        # solve for Temperature:
        t = solve_tridiagonal(a, b, c, d)
        temp_grid[i][:] = t # store in grid
        
        
        # plot:
        # ax.plot(t, x)
        # ax.set_ylabel('Altitude')
        # ax.set_xlabel('Temperature')
        
        
    cs = ax.contourf(times/24, 100+x*40, np.array(temp_grid.T))
    ax.set_ylabel('Altitude (km)')
    ax.set_xlabel('Time (days)')
    cbar = plt.colorbar(cs, label = 'Temperature (K)')
    
    plotfile = 'conduction_v1.png'
    print('writing : ',plotfile)    
    fig.savefig(plotfile)