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
import os
import logging
log = logging.getLogger(__name__)

from scipy.integrate import ode

import neutronics
import thermal_hydraulics

import testin
from inp import sim_info

from ur import units


log.info("Simulation starting.")
np.set_printoptions(precision=testin.np_precision)

ne = neutronics.Neutronics(testin.fission_iso,
                           testin.spectrum,
                           testin.n_pg,
                           testin.n_dg)

th = thermal_hydraulics.ThermalHydraulics()

si = sim_info.SimInfo(t0=testin.t0, tf=testin.tf, dt=testin.dt,
                      components=th._params._components)
n_components = len(si.components)
n_entries = 1 + testin.n_pg + testin.n_dg + n_components

_y = np.zeros(shape=(si.timesteps(), n_entries), dtype=float)

_temp = units.Quantity(np.zeros(shape=(si.timesteps(), n_components),
                                dtype=float), 'kelvin')

for key, val in th._params._init_temps.iteritems():
    _temp[0][si.components[key]] = val


def update_n(t, y_n):
    """This function updates the neutronics block.
    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y_n: The array that solves the neutronics block at time t
    :type y_n: np.ndarray.
    """
    n_n = len(y_n)
    _y[t/si.dt][:n_n] = y_n


def update_th(t, y_n, y_th):
    """This function updates the thermal hydraulics block.
    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y_th: The array that solves thermal hydraulics block at time t
    :type y_th: thp.thdarray.
    """
    _temp[int(t/si.dt)][:] = y_th
    n_n = len(y_n)
    _y[t/si.dt][n_n:] = y_th


def f_n(t, y, coeffs):
    """Returns the neutronics solution at time t, based on temperature
    coefficients of reactivity.
    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y: TODO
    :type y: np.ndarray
    :param coeffs: a dictionary of component names and coefficients
    :type coeffs: dict.
    """
    f = np.zeros(shape=(1+testin.n_pg + testin.n_dg,), dtype=float)
    i = 0
    f[i] = ne.dpdt(t, si.dt, _temp, coeffs, y[0], y[1:testin.n_pg+1])
    for j in range(0, testin.n_pg):
        i += 1
        f[i] = ne.dzetadt(t, y[0], y[i], j)
    for k in range(0, testin.n_dg):
        i += 1
        f[i] = ne.dwdt(y[0], y[i], k)
    return f


def f_th(t, y_th):
    """Returns the thermal hydraulics solution at time t
    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y: TODO
    :type y: np.ndarray
    """
    f = units.Quantity(np.zeros(shape=(n_components,), dtype=float),
                       'kelvin / second')
    power = _y[t/si.dt][0]
    o_i = 1+testin.n_pg
    o_f = 1+testin.n_pg+testin.n_dg
    omegas = _y[t/si.dt][o_i:o_f]
    for name, num in si.components.iteritems():
        print name
        f[num] = th.dtempdt(name, y_th, power, omegas, si.components)
    return f


def y0():
    """The initial conditions for y"""
    i = 0
    f = np.zeros(shape=(n_entries,), dtype=float)
    f[i] = 1.0  # real power is 236 MWth, but normalized is 1
    for j in range(0, testin.n_pg):
        i += 1
        f[i] = 0
    for k in range(0, testin.n_dg):
        i += 1
        f[i] = 0
    for name, num in si.components.iteritems():
        f[i+num+1] = _temp[0][num].magnitude
    assert len(f) == n_entries
    _y[0] = f
    return f


def y0_n():
    """The initial conditions for y_n, the neutronics sub-block of y"""
    idx = testin.n_pg+testin.n_dg + 1
    # print "len y0_n : " + str(idx)
    y = y0()[:idx]
    return y


def y0_th():
    """The initial conditions for y_th, the thermal hydraulics sub-block of
    y"""
    tidx = testin.n_pg+testin.n_dg + 1
    y = y0()[tidx:]
    return y


def solve():
    """Conducts the solution step, based on the dopri5 integrator in scipy"""
    n = ode(f_n).set_integrator('dopri5')
    n.set_initial_value(y0_n(), si.t0).set_f_params(testin.coeffs)
    th = ode(f_th).set_integrator('dopri5')
    th.set_initial_value(y0_th(), si.t0)
    while n.successful() and n.t*units.seconds < testin.tf:
        n.integrate(n.t+si.dt)
        update_n(n.t, n.y)
        th.integrate(th.t+si.dt)
        update_th(n.t, n.y, th.y)
    print("Reactivity : ", ne._rho)
    print(ne._dd.lambdas())
    print("Final Result : ", _y)
    print("Final Temps : ", _temp)
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
    """Returns a nice looking color map"""
    values = range(n_entries)
    jet = plt.get_cmap('jet')
    c_norm = colors.Normalize(vmin=0, vmax=values[-1])
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=jet)
    color_val = scalar_map.to_rgba(values[num])
    return color_val


def plot(y):
    """Creates plots for interesting values in the simulation.
    :param y: The full solution array
    :type y: np.ndarray"""
    x = np.arange(si.t0, testin.tf+si.dt, si.dt)
    plot_power(x, y)
    plot_reactivity(x)
    plot_zetas(x, y)
    plot_omegas(x, y)
    plot_temps_together(x, y)
    plot_temps_separately(x, y)


def plot_reactivity(x):
    """Plots the reactivity
    :param x: The time series
    :type x: np.ndarray"""
    plt.plot(x, ne._rho.values(), color=my_colors(1), marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Reactivity [$Delta$k/k]")
    plt.title("Reactivity [$Delta$k/k]")
    saveplot("reactivity", plt)


def plot_power(x, y):
    power = y[:, 0]
    plt.plot(x, power, color=my_colors(1), marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Power [units]")
    plt.title("Power [units]")
    saveplot("power", plt)


def plot_temps_together(x, y):
    for name, num in si.components.iteritems():
        idx = 1 + testin.n_pg + testin.n_dg + num
        plt.plot(x, y[:, idx], label=name, color=my_colors(num), marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature of Each Component")
    saveplot("temps", plt)


def plot_temps_separately(x, y):
    for name, num in si.components.iteritems():
        idx = 1 + testin.n_pg + testin.n_dg + num
        plt.plot(x, y[:, idx], label=name, color=my_colors(num), marker='.')
        plt.xlabel("Time [s]")
        plt.ylabel("Temperature [K]")
        plt.title("Temperature of "+name)
        saveplot(name+" Temp[K]", plt)


def plot_zetas(x, y):
    for num in range(0, testin.n_pg):
        idx = num + 1
        plt.plot(x, y[:, idx], color=my_colors(num), marker='.')
    plt.xlabel(r'Time $[s]$')
    plt.ylabel("Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    plt.title("Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    saveplot("zetas", plt)


def plot_omegas(x, y):
    for num in range(0, testin.n_dg):
        idx = 1 + testin.n_pg + num
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
