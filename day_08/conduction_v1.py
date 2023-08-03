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
    Q = np.zeros(len(x))
    for i in range(len(x)):
        if x[i] > 2 and x[i] < 8:
                Q[i] = -100
    lam = 10
    dz = x[1] - x[0]
    dz2 = dz*dz
    d[:] = -Q*dz2/lam

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
    a[-1] = 0
    b[-1] = 1
    c[-1] = 0
    d[-1] = t_upper

    # Add a source term:
    
    # solve for Temperature:
    t = solve_tridiagonal(a, b, c, d)

    # plot:
    fig = plt.figure(figsize = (10,10))
    ax = fig.add_subplot(211)
    ax.plot(t, x)
    ax.set_ylabel('x')
    ax.set_xlabel('Temperature')
    
    ax2 = fig.add_subplot(212)
    ax2.plot(Q, x)
    ax2.set_ylabel('x')
    ax2.set_xlabel('Q')
    ax = fig.add_subplot(111)

    ax.plot(x, t)

    plotfile = 'conduction_v1.png'
    print('writing : ',plotfile)    
    fig.savefig(plotfile)
    plt.close()
    
    
    
