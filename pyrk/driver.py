#! /usr/bin/env python

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
This is an example driver for the simulation. It should soon be refactored to
result in an input file, an input parser, a solver interface, and output
scripts.
"""

import numpy as np
from scipy.integrate import ode
import importlib
import argparse
from utilities import logger
from utilities.logger import pyrklog
from inp import sim_info
from utilities.ur import units
from utilities import plotter
import os


def update_n(t, y_n, si):
    """This function updates the neutronics block.

    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y_n: The array that solves the neutronics block at time t
    :type y_n: np.ndarray.
    """
    t_idx = si.timer.t_idx(t*units.seconds)
    n_n = len(y_n)
    si.y[t_idx][:n_n] = y_n


def update_th(t, y_n, y_th, si):
    """This function updates the thermal hydraulics block.

    :param t: the time [s] at which the update is occuring.
    :type t: float.

    :param y_th: The array that solves thermal hydraulics block at time t
    :type y_th: np.ndarray.
    """
    t_idx = si.timer.t_idx(t*units.seconds)
    for idx, comp in enumerate(si.components):
        comp.update_temp(t_idx, y_th[idx]*units.kelvin)
    n_n = len(y_n)
    si.y[t_idx][n_n:] = y_th


def f_n(t, y, si):
    """Returns the neutronics block solution at time t

    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y: solution vector
    :type y: np.ndarray
    """
    n_n = 1 + si.n_pg + si.n_dg
    end_pg = 1 + si.n_pg
    f = np.zeros(shape=(n_n,), dtype=float)
    i = 0
    f[i] = si.ne.dpdt(si.timer.ts,
                      si.components,
                      y[0],
                      y[1:end_pg])
    for j in range(0, si.n_pg):
        i += 1
        f[i] = si.ne.dzetadt(t, y[0], y[i], j)
    assert(i == end_pg-1)
    for k in range(0, si.n_dg):
        i += 1
        f[i] = si.ne.dwdt(y[0], y[i], k)
    return f


def f_th(t, y_th, si):
    """Returns the thermal hydraulics solution at time t

    :param t: the time [s] at which the update is occuring.
    :type t: float.
    :param y: the solution vector
    :type y: np.ndarray
    :param si: the simulation info object
    :type si: SimInfo
    """
    t_idx = si.timer.t_idx(t*units.seconds)
    f = units.Quantity(np.zeros(shape=(si.n_components(),), dtype=float),
                       'kelvin / second')
    power = si.y[t_idx][0]
    o_i = 1+si.n_pg
    o_f = 1+si.n_pg+si.n_dg
    omegas = si.y[t_idx][o_i:o_f]
    for idx, comp in enumerate(si.components):
        f[idx] = si.th.dtempdt(component=comp,
                               power=power,
                               omegas=omegas,
                               t_idx=t_idx)
    return f


def y0(si):
    """The initial conditions for y

    :param si: the simulation info object
    :type si: SimInfo
    """
    i = 0
    f = np.zeros(shape=(si.n_entries(),), dtype=float)
    f[i] = 1.0  # power is normalized is 1
    for j in range(0, si.n_pg):
        i += 1
        f[i] = f[0] * \
            si.ne._pd.betas()[j]/(si.ne._pd.lambdas()[j]*si.ne._pd.Lambda())
    for k in range(0, si.n_dg):
        i += 1
        f[i] = 0
    for idx, comp in enumerate(si.components):
        f[i+idx+1] = comp.T0.magnitude
    assert len(f) == si.n_entries()
    si.y[0] = f
    return f


def y0_n(si):
    """Initial conditions for y_n, the neutronics sub-block of y

    :param si: the simulation info object
    :type si: SimInfo
    """
    idx = si.n_pg+si.n_dg + 1
    y = y0(si)[:idx]
    return y


def y0_th(si):
    """Initial conditions for y_th, the thermal hydraulics sub-block of y

    :param si: the simulation info object
    :type si: SimInfo
    """
    thidx = si.n_pg+si.n_dg + 1
    y = y0(si)[thidx:]
    return y


def solve(si, y, infile):
    """Conducts the solution step, based on the dopri5 integrator in scipy

    :param si: the simulation info object
    :type si: SimInfo
    :param y: the solution vector
    :type y: np.ndarray
    :param infile: the imported infile module
    :type infile: imported module
    """
    n = ode(f_n).set_integrator('dopri5')
    n.set_initial_value(y0_n(si), si.timer.
                        t0.magnitude)
    n.set_f_params(si)
    th = ode(f_th).set_integrator('dopri5', nsteps=infile.nsteps)
    th.set_initial_value(y0_th(si), si.timer.t0.magnitude)
    th.set_f_params(si)
    while (n.successful()
           and n.t < si.timer.tf.magnitude
           and th.t < si.timer.tf.magnitude):
        si.timer.advance_one_timestep()
        n.integrate(si.timer.current_time().magnitude)
        update_n(n.t, n.y, si)
        th.integrate(si.timer.current_time().magnitude)
        update_th(th.t, n.y, th.y, si)
    return si.y


def log_results(si):
    pyrklog.info("\nReactivity : \n"+str(si.ne._rho))
    pyrklog.info("\nFinal Result : \n"+np.array_str(si.y))
    for comp in si.components:
        pyrklog.info("\n" + comp.name + ":\n" + np.array_str(comp.T.magnitude))
    pyrklog.info("\nPrecursor lambdas: \n"+str(si.ne._pd.lambdas()))
    pyrklog.info("\nDelayed neutron frac: \n"+str(si.ne._pd.beta()))
    pyrklog.info("\nPrecursor betas: \n"+str(si.ne._pd.betas()))
    pyrklog.info("\nDecay kappas: \n"+str(si.ne._dd.kappas()))
    pyrklog.info("\nDecay lambdas: \n"+str(si.ne._dd.lambdas()))


def print_logo(curr_dir):
    filename = os.path.join(curr_dir, 'logo.txt')
    with open(filename, 'r') as logo:
        pyrklog.critical("\nWelcome to PyRK.\n" +
                         "(c) Kathryn D. Huff\n" +
                         "Your simulation is starting.\n" +
                         "Perhaps it's time for a coffee.\n" +
                         logo.read())


def load_infile(infile_path):
    """Loads the input file as a python package import based on the path

    :param infile_path: path to the infile
    :type infile_path: string
    """
    import os.path
    import sys
    file_dir = os.path.dirname(infile_path)
    sys.path.append(file_dir)
    file_name = os.path.basename(infile_path).rstrip('.py')
    infile = importlib.import_module(file_name)
    return infile


def main(args, curr_dir):
    np.set_printoptions(precision=5, threshold=np.inf)
    logger.set_up_pyrklog(args.logfile)
    infile = load_infile(args.infile)
    si = sim_info.SimInfo(timer=infile.ti,
                          components=infile.components,
                          iso=infile.fission_iso,
                          e=infile.spectrum,
                          n_precursors=infile.n_pg,
                          n_decay=infile.n_dg,
                          kappa=infile.kappa,
                          feedback=infile.feedback,
                          rho_ext=infile.rho_ext,
                          plotdir=args.plotdir)
    print_logo(curr_dir)
    sol = solve(si=si, y=si.y, infile=infile)
    log_results(si)
    plotter.plot(sol, si)
    pyrklog.critical("\nSimulation succeeded.\n")


"""Run it as a script"""
if __name__ == "__main__":
    curr_dir = os.path.dirname(__file__)
    ap = argparse.ArgumentParser(description='PyRK parameters')
    ap.add_argument('--infile', help='the name of the input file',
                    default='input')
    ap.add_argument('--logfile', help='the name of the log file',
                    default='pyrk.log')
    ap.add_argument(
        '--plotdir',
        help='the name of the directory of output plots',
        default='images')
    ap.add_argument('--outfile', help='the name of the output database',
                    default='pyrk.h5')
    args = ap.parse_args()
    main(args, curr_dir)
