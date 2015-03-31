# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This is an example driver for the simulation. It should soon be refactored to
result in an input file, an input parser, a solver interface, and output
scripts.
"""

import numpy as np
from scipy.integrate import ode
import importlib

import thermal_hydraulics
from utils.logger import logger
from inp import sim_info
from ur import units
from utils import plotter
import testin


np.set_printoptions(precision=testin.np_precision)

th = thermal_hydraulics.ThermalHydraulics()

infile = importlib.import_module("testin")
si = sim_info.SimInfo(t0=testin.t0,
                      tf=testin.tf,
                      dt=testin.dt,
                      components=th._params._components,
                      iso=testin.fission_iso,
                      e=testin.spectrum,
                      n_precursors=testin.n_pg,
                      n_decay=testin.n_dg,
                      th=th)

n_components = len(si.components)

_y = np.zeros(shape=(si.timesteps(), si.n_entries()), dtype=float)

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
    t_idx = int(t/si.dt.magnitude)
    n_n = len(y_n)
    _y[t_idx][:n_n] = y_n


def update_th(t, y_n, y_th):
    """This function updates the thermal hydraulics block.
    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y_th: The array that solves thermal hydraulics block at time t
    :type y_th: thp.thdarray.
    """
    t_idx = int(t/si.dt.magnitude)
    _temp[int(t_idx)][:] = units.Quantity(y_th, 'kelvin')
    n_n = len(y_n)
    _y[int(t_idx)][n_n:] = y_th


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
    n_n = 1 + si.n_pg + si.n_dg
    end_pg = 1 + si.n_pg
    f = np.zeros(shape=(n_n,), dtype=float)
    i = 0
    f[i] = si.ne.dpdt(t*units.second, si.dt, _temp, coeffs, y[0], y[1:end_pg])
    for j in range(0, si.n_pg):
        i += 1
        f[i] = si.ne.dzetadt(t, y[0], y[i], j)
    assert(i == end_pg-1)
    for k in range(0, si.n_dg):
        i += 1
        f[i] = si.ne.dwdt(y[0], y[i], k)
    return f


def f_th(t, y_th):
    """Returns the thermal hydraulics solution at time t
    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y: TODO
    :type y: np.ndarray
    """
    t_idx = int(t/si.dt.magnitude)
    f = units.Quantity(np.zeros(shape=(n_components,), dtype=float),
                       'kelvin / second')
    power = _y[t_idx][0]
    o_i = 1+si.n_pg
    o_f = 1+si.n_pg+si.n_dg
    omegas = _y[t_idx][o_i:o_f]
    for name, num in si.components.iteritems():
        f[num] = th.dtempdt(name, y_th, power, omegas, si.components)
    return f


def y0():
    """The initial conditions for y"""
    i = 0
    f = np.zeros(shape=(si.n_entries(),), dtype=float)
    f[i] = 1.0  # real power is 236 MWth, but normalized is 1
    for j in range(0, si.n_pg):
        i += 1
        f[i] = 0
    for k in range(0, si.n_dg):
        i += 1
        f[i] = 0
    for name, num in si.components.iteritems():
        f[i+num+1] = _temp[0][num].magnitude
    assert len(f) == si.n_entries()
    _y[0] = f
    return f


def y0_n():
    """The initial conditions for y_n, the neutronics sub-block of y"""
    idx = si.n_pg+si.n_dg + 1
    y = y0()[:idx]
    return y


def y0_th():
    """The initial conditions for y_th, the thermal hydraulics sub-block of
    y"""
    tidx = si.n_pg+si.n_dg + 1
    y = y0()[tidx:]
    return y


def solve():
    """Conducts the solution step, based on the dopri5 integrator in scipy"""
    n = ode(f_n).set_integrator('dopri5')
    n.set_initial_value(y0_n(), si.t0.magnitude).set_f_params(infile.coeffs)
    th = ode(f_th).set_integrator('dopri5', nsteps=si.timesteps())
    th.set_initial_value(y0_th(), si.t0.magnitude)
    while n.successful() and n.t < si.tf.magnitude:
        n.integrate(n.t+si.dt.magnitude)
        update_n(n.t, n.y)
        th.integrate(th.t+si.dt.magnitude)
        update_th(n.t, n.y, th.y)

    return _y


def log_results():
    logger.info("\nReactivity : \n"+str(si.ne._rho))
    logger.info("\nFinal Result : \n"+str(_y))
    logger.info("\nFinal Temps : \n"+str(_temp))
    logger.info("\nPrecursor lambdas: \n"+str(si.ne._pd.lambdas()))
    logger.info("\nDelayed neutron frac: \n"+str(si.ne._pd.beta()))
    logger.info("\nPrecursor betas: \n"+str(si.ne._pd.betas()))
    logger.info("\nDecay kappas: \n"+str(si.ne._dd.kappas()))
    logger.info("\nDecay lambdas: \n"+str(si.ne._dd.lambdas()))


"""Run it as a script"""
if __name__ == "__main__":
    with open('logo.txt', 'r') as logo:
        logger.critical("\nWelcome to PyRK.\n" +
                        "(c) Kathryn D. Huff\n" +
                        "Your simulation is starting.\n" +
                        "Perhaps it's time for a coffee.\n" +
                        logo.read())
    sol = solve()
    log_results()
    plotter.plot(sol, si)
    logger.critical("\nSimulation succeeded.\n")
