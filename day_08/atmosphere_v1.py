#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from tridiagonal import solve_tridiagonal
from densityarray import build_dens

# ----------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------

if __name__ == "__main__":

    dx = 4

    # set x with 1 ghost cell on both sides:
    x = 100 + np.arange(-dx, 400 + 2*dx, dx)
    # alt = 100+x*40

    t_lower = 200.0 
    t_upper = 1000.0

    nPts = len(x)

    # set default coefficients for the solver:
    a = np.zeros(nPts) - 1
    b = np.zeros(nPts) + 2
    c = np.zeros(nPts) - 1
    d = np.zeros(nPts)
    
    # additions
    lam = 80
    
    # time dependent term
    nDays = 27
    dt = 1
    times = np.arange(0, nDays*24, dt)
    lon = 0.0

    # temperature grid to store temps at different times
    temp_grid = np.zeros([len(times), len(x)])
    dens_grid_N2 = np.zeros([len(times), len(x)])
    dens_grid_O2 = np.zeros([len(times), len(x)])
    dens_grid_O = np.zeros([len(times), len(x)])
    O2_m_AMU = 32 
    O2_n0 = 0.3e19
    O_m_AMU = 16
    O_n0 = 1e18
    
    # diurnal and semidurnal
    AmpDi = 10
    AmpSd = 5
    PhaseDi = np.pi/2
    PhaseSd = 3*np.pi/2
    
    # adding wavelengths
    f107 = 100 + 50/(25*365)*times + 25*np.sin(times/(27*24)*2*np.pi)

    for i, hour in enumerate(times):
        ut = hour % 24
        local_time = lon/15 + ut
        
        factor = -np.cos(local_time/24*2*np.pi)
        if factor < 0:
            factor = 0
            
        sun_heat = f107[i]*.4/100
    
        # setting Q for only some altitudes
        cond = np.logical_and(x < 400, x > 200)
        
        QEUV = np.zeros(nPts)    
        QEUV[cond] = -sun_heat*factor
        
        Qback = np.zeros(nPts)
        Qback[cond] = -0.4
       
        Qtotal = Qback + QEUV
        
        # change in altitude and final d column for tridiagonal solver
        dz = x[1] - x[0]
        dz2 = dz*dz
        d[:] = -Qtotal*dz2/lam

        # boundary conditions (bottom - fixed):
        a[0] = 0
        b[0] = 1
        c[0] = 0
        d[0] = t_lower + AmpDi*np.sin(local_time/24*2*np.pi + PhaseDi) + \
                AmpSd*np.sin(local_time/24*2*2*np.pi + PhaseSd)

        # top - fixed:
        a[-1] = 1
        b[-1] = -1
        c[-1] = 0
        d[-1] = 0
    
        # solve for Temperature:
        t = solve_tridiagonal(a, b, c, d)
        temp_grid[i][:] = t # store in grid
        dens_grid_N2[i][:] = build_dens(t, x)
        dens_grid_O2[i][:] = build_dens(t, x, O2_m_AMU, O2_n0)
        dens_grid_O[i][:] = build_dens(t, x, O_m_AMU, O_n0)
        

    # back in main
    # instantiate figure
    fig = plt.figure(figsize = (12,10))
    
    items = ['Temp', 'N2', 'O2', 'O']
    titles = ['Temperature', 'Density of N2', 'Density of O2', 'Density of O']
    colorbar_label = ['Temp. (K)', 'Density (per cubic meter)', \
                      'Density (per cubic meter)', 'Density (per cubic meter)']
    grids = {'Temp': temp_grid, 'N2': np.log10(dens_grid_N2), \
             'O2': np.log10(dens_grid_O2), 'O': np.log10(dens_grid_O)}

    for i in range(4):
        ax = plt.subplot(2, 2, i + 1)
        cs = ax.contourf(times/24, x, np.array(grids[items[i]]).T)
        ax.set_ylabel('Altitude (km)')
        ax.set_xlabel('Time (days)')
        ax.set_title(titles[i])
        cbar = plt.colorbar(cs, label = colorbar_label[i])
    
    plotfile = 'atmosphere_v1.png'
    print('writing : ',plotfile)    
    fig.savefig(plotfile)
        
    