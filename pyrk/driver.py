# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This is an example driver for the simulation. It should soon be refactored to
result in an input file, an input parser, a solver interface, and output
scripts.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
from matplotlib.pyplot import legend
import os
import logging
log = logging.getLogger(__name__)

from scipy.integrate import ode

import neutronics
import thermal_hydraulics

from testin import *
from inp import sim_info


log.info("Simulation starting.")
np.set_printoptions(precision=np_precision)

ne = neutronics.Neutronics(fission_iso,
                           spectrum,
                           n_precursor_groups,
                           n_decay_groups)


th = thermal_hydraulics.ThermalHydraulics()

si = sim_info.SimInfo(t0=t0, tf=tf, dt=dt, components=th._params._components)
n_components = len(si.components)
n_entries = 1 + n_precursor_groups + n_decay_groups + n_components

_y = np.zeros(shape=(si.timesteps(), n_entries), dtype=float)

_temp = np.zeros(shape=(si.timesteps(), n_components), dtype=float)

for key, val in th._params._init_temps.iteritems():
    _temp[0][si.components[key]] = val


def update_n(t, y_n):
    n_n = len(y_n)
    _y[t/dt][:n_n] = y_n


def update_th(t, y_n, y_th):
    _temp[int(t/dt)][:] = y_th
    n_n = len(y_n)
    _y[t/dt][n_n:] = y_th


def f_n(t, y, coeffs):
    f = np.zeros(shape=(1+n_precursor_groups + n_decay_groups,), dtype=float)
    i = 0
    f[i] = ne.dpdt(t, dt, _temp, coeffs, y[0], y[1:n_precursor_groups+1])
    # print str(f)
    for j in range(0, n_precursor_groups):
        i += 1
        f[i] = ne.dzetadt(t, y[0], y[i], j)
    # print str(f)
    for k in range(0, n_decay_groups):
        i += 1
        f[i] = ne.dwdt(y[0], y[i], k)
    # print str(f)
    # print "type of f_n : "+ str(type(f.values()))
    # print "len of f_n : "+ str(len(f.values()))
    return f


def f_th(t, y_th):
    f = np.zeros(shape=(n_components,), dtype=float)
    power = _y[t/dt][0]
    o_i = 1+n_precursor_groups
    o_f = 1+n_precursor_groups+n_decay_groups
    omegas = _y[t/dt][o_i:o_f]
    for name, num in si.components.iteritems():
        f[num] = th.dtempdt(name, y_th, power, omegas, si.components)
    # print "type of f_th : "+ str(type(f.values()))
    return f


def y0():
    i = 0
    f = np.zeros(shape=(n_entries,), dtype=float)
    f[i] = 1.0  # real power is 236 MWth, but normalized is 1
    for j in range(0, n_precursor_groups):
        i += 1
        f[i] = 0
    for k in range(0, n_decay_groups):
        i += 1
        f[i] = 0
    for name, num in si.components.iteritems():
        f[i+num+1] = _temp[0][num]
    assert len(f) == n_entries
    _y[0] = f
    return f


def y0_n():
    idx = n_precursor_groups+n_decay_groups + 1
    # print "len y0_n : " + str(idx)
    y = y0()[:idx]
    return y


def y0_th():
    tidx = n_precursor_groups+n_decay_groups + 1
    y = y0()[tidx:]
    return y


def solve():
    n = ode(f_n).set_integrator('dopri5')
    n.set_initial_value(y0_n(), t0).set_f_params(coeffs)
    th = ode(f_th).set_integrator('dopri5')
    th.set_initial_value(y0_th(), t0)
    while n.successful() and n.t < tf:
        n.integrate(n.t+dt)
        update_n(n.t, n.y)
        th.integrate(th.t+dt)
        update_th(n.t, n.y, th.y)
    print("Final Result : ",_y)
    print("Final Temps : ",_temp)
    print("Precursor lambdas:")
    print(ne._pd.lambdas())
    print("Precursor betas:")
    print(ne._pd.betas())
    print("Decay kappas")
    print(ne._dd.kappas())
    print("Decay lambdas")
    print(ne._dd.lambdas())
    return _y


def my_colors(num):
    values = range(n_entries)
    jet = plt.get_cmap('jet')
    cNorm = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    colorVal = scalarMap.to_rgba(values[num])
    return colorVal


def plot(y):
    x = np.arange(t0, tf+dt, dt)
    plot_power(x, y)
    plot_zetas(x, y)
    plot_omegas(x, y)
    plot_temps_together(x, y)
    plot_temps_separately(x, y)


def plot_power(x, y):
    power = y[:, 0]
    plt.plot(x, power, color=my_colors(1), marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Power [units]")
    plt.title("Power [units]")
    saveplot("power", plt)


def plot_temps_together(x, y):
    for name, num in si.components.iteritems():
        idx = 1 + n_precursor_groups + n_decay_groups + num
        plt.plot(x, y[:, idx], label=name, color=my_colors(num), marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature of Each Component")
    saveplot("temps", plt)


def plot_temps_separately(x, y):
    for name, num in si.components.iteritems():
        idx = 1 + n_precursor_groups + n_decay_groups + num
        plt.plot(x, y[:, idx], label=name, color=my_colors(num), marker='.')
        plt.xlabel("Time [s]")
        plt.ylabel("Temperature [K]")
        plt.title("Temperature of "+name)
        saveplot(name+" Temp[K]", plt)


def plot_zetas(x, y):
    for num in range(0, n_precursor_groups):
        idx = num + 1
        plt.plot(x, y[:, idx], color=my_colors(num), marker='.')
    plt.xlabel(r'Time $[s]$')
    plt.ylabel("Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    plt.title("Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    saveplot("zetas", plt)


def plot_omegas(x, y):
    for num in range(0, n_decay_groups):
        idx = 1 + n_precursor_groups + num
        plt.plot(x, y[:, idx], color=my_colors(num), marker='.')
    plt.xlabel(r'Time $[s]$')
    plt.ylabel(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
    plt.title(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
    saveplot("omegas", plt)


def saveplot(name, plt):
    plotdir = 'images'
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    plt.savefig(str(plotdir+"/"+name+'.pdf'), bbox_inches='tight')
    plt.savefig(str(plotdir+"/"+name+'.eps'), bbox_inches='tight')
    plt.clf()

"""Run it as a script"""
if __name__ == "__main__":
    sol = solve()
    a = plot(sol)
