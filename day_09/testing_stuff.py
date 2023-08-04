# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:52:27 2023

@author: emide
"""

import numpy as np 
import scipy.linalg as la
import scipy.sparse as sparse
import opinf
import matplotlib.pyplot as plt
import matplotlib
import time as timepkg

start = timepkg.time()

font = {'family' : 'serif',
        'size'   : 12}

matplotlib.rc('font', **font)
matplotlib.rc('xtick', labelsize=12) 
matplotlib.rc('ytick', labelsize=12) 

# load simulation data using numpy 
data = np.load("conduction_v6_data.npy")

# use 100 snapshots for training and 43 for testing
Q_train = data[:, :100]
Q_test = data[:, 100:]
print("shape of the simulation data = ", np.shape(data))
print("shape of the training simulation data = ", np.shape(Q_train))
print("shape of the testing simulation data = ", np.shape(Q_test))

# altitude in km
x = np.load("conduction_v6_alt.npy")/1000
dx = x[1] - x[0]
print(f"Spatial step size δx = {dx} km")

# time in hr
time = np.load("conduction_v6_time.npy")[:-1]
dt = time[1] - time[0]
print(f"Temporal step size δt = {dt} hr")

# inputs 
inputs = np.load("conduction_v6_lower_bc.npy")[:-1]

colors = plt.cm.viridis(np.linspace(0, 1, 10))

# plot the training data
fig, ax = plt.subplots(figsize=(9, 4))

# plot up to noon
for ii, tt in enumerate(np.arange(0, 100, 10)):
    ax.plot(x, Q_train[:, tt], linewidth=2, label="$q(x, t=$" + str(int(time[tt])) + "hr)", color=colors[ii])

# hide axis
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# set axis limits 
ax.set_xlim(100, 500)
ax.set_ylim(100, 700)

# axis legends
ax.set_xlabel("$x$ [km]")
ax.set_ylabel("$q(x, t)$ [K]")

# add legend
legend = ax.legend(ncols=1, fancybox=False, shadow=False, fontsize=10,  bbox_to_anchor=(1, 1))
legend.get_frame().set_alpha(0)

# add title
_= ax.set_title("Snapshot data for training")

# Compute the POD basis, using the residual energy tolerance to select r.
basis = opinf.pre.PODBasis().fit(Q_train, residual_energy = 1e-18)
print(basis)

# Check the decay of the singular values.
_ = basis.plot_svdval_decay()

# based on the criteria we set above
basis.r = 23

# approximate the dx/dt using forward euler finite differencing
training_data_ddt = (Q_train[:, 1:] - Q_train[:, :-1])/dt

# learn reduced model.
rom = opinf.ContinuousOpInfROM("AB")
rom.fit(basis=basis, states=Q_train[:, :-1], ddts=training_data_ddt, regularizer=1, inputs=inputs[1:100])

# Express the initial condition in the coordinates of the basis.
q0_ = rom.encode(Q_train[:, 0])

# Solve the reduced-order model using BDF
Q_ROM = rom.predict(state0=q0_, t=time, decode=True, input_func=inputs)

# plot the training data
fig, ax = plt.subplots(nrows=2, figsize=(8, 7))

# plot up to noon
for ii, tt in enumerate(np.arange(0, 100, 10)):
    ax[0].plot(x, Q_train[:, tt], linewidth=2, label="$q(x, t=$" + str(tt) + "hr)", color=colors[ii])
    ax[1].plot(x, Q_ROM[:, tt], linewidth=2, label="$q(x, t=$" + str(tt) + "hr)", color=colors[ii])

# hide axis
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)
ax[1].spines['top'].set_visible(False)

# set axis limits 
ax[0].set_xlim(100, 500)
ax[1].set_xlim(100, 500)
ax[0].set_ylim(100, 700)
ax[1].set_ylim(100, 700)

# axis legends
ax[0].set_xlabel("$x$ [km]")
ax[0].set_ylabel("$q(x, t)$ [K]")
ax[1].set_xlabel("$x$ [km]")
ax[1].set_ylabel("$q(x, t)$ [K]")

# add legend
legend = ax[0].legend(ncols=1, fancybox=False, shadow=False, fontsize=10,  bbox_to_anchor=(1, 1))
legend.get_frame().set_alpha(0)
legend = ax[1].legend(ncols=1, fancybox=False, shadow=False, fontsize=10,  bbox_to_anchor=(1, 1))
legend.get_frame().set_alpha(0)


# add title
_= ax[0].set_title("Snapshot data for training")
_= ax[1].set_title("ROM reconstruction")
plt.tight_layout()

fig, ax = plt.subplots(ncols=3, sharey=True, figsize=(16, 4))
pos = ax[0].pcolormesh(x, time, data.T, vmin=100, vmax=700)
cbar = fig.colorbar(pos)
cbar.ax.set_ylabel('$q(x, t)$', rotation=90)
pos = ax[1].pcolormesh(x, time, Q_ROM.T, vmin=100, vmax=700)
cbar = fig.colorbar(pos)
cbar.ax.set_ylabel('$q(x, t)$', rotation=90)

pos = ax[2].pcolormesh(x, time, 100*np.abs(data.T - Q_ROM.T)/np.abs(data.T))
cbar = fig.colorbar(pos)
cbar.ax.set_ylabel(r"Relative Error %", rotation=90)

ax[0].axhline(time[100], linewidth=2, color="white", linestyle="--")
ax[1].axhline(time[100], linewidth=2, color="white", linestyle="--")
ax[2].axhline(time[100], linewidth=2, color="white", linestyle="--")
ax[0].set_xlabel("$x$ [km]")
ax[1].set_xlabel("$x$ [km]")
ax[2].set_xlabel("$x$ [km]")
ax[0].set_ylabel("$t$ [hr]")

_ = ax[0].set_title("FOM")
_ = ax[1].set_title("ROM")
_ = ax[2].set_title("Relative Error")

end_time = timepkg.time()

print(end_time - start, ' seconds')
