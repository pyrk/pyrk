# Licensed under a 3-clause BSD-style license - see LiCENSE.rst
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
from cycler import cycler
plt.style.use(os.path.join(os.path.dirname(__file__), 'plotting.mplstyle'))

def color_list():
    return ["#332288", "#117733", "#44AA99", "#88CCEE", "#DDCC77", "#CC6677", "#AA4499", "#882255"]

def plot(y, si):
    """Creates plots for interesting values in the simulation.
    :param y: The full solution array
    :type y: np.ndarray"""
    x = si.timer.series.magnitude
    plot_power(x, y, si)
    plot_reactivity(x, si)
    plot_power_w_reactivity(x=x, y=y, si=si)
    plot_zetas(x, y, si)
    if si.ne._ndg > 0:
        plot_omegas(x, y, si)
    plot_temps_together(x, y, si)
    plot_temps_separately(x, y, si)


def plot_reactivity(x, si):
    """Plots the reactivity
    :param x: The time series
    :type x: np.ndarray"""
    plt.plot(x, si.ne._rho,marker='.',color='#332288')
    plt.xlabel("Time [s]")
    plt.ylabel(r"Reactivity [$\Delta k/k$]")
    plt.title(r"Reactivity [$\Delta k/k$]")
    saveplot("reactivity", plt, si.plotdir)


def plot_power(x, y, si):
    power = y[:, 0]
    plt.plot(x, power, marker='.',color='#117733')
    plt.xlabel("Time [s]")
    plt.ylabel("Power [units]")
    plt.title("Power [units]")
    saveplot("power", plt, si.plotdir)


def plot_power_w_reactivity(x, si, y):
    power = y[:, 0]
    rho = si.ne._rho
    fig,ax1=plt.subplots()
    ax1.plot(x, power, marker='.', label="Power",color='#44AA99')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Power')
    ax1.tick_params(axis='y')

    ax2=ax1.twinx()
    ax2.plot(x, rho, marker='.',
             label="External Reactivity",color="#88CCEE")
    ax2.set_ylabel(r'Reactivity [$\Delta k$]')
    ax2.tick_params(axis='y')

    ax1.legend(loc='upper right')
    ax2.legend(loc='upper left')
    plt.title(r"Power and Reactivity [$\Delta k$]")
    saveplot("pow_and_rho", plt, si.plotdir)


def plot_temps_together(x, y, si):
    for num, comp in enumerate(si.components):
        idx = 1 + si.ne._npg + si.ne._ndg + num
        plt.plot(x, y[:, idx], label=comp.name, marker='.')
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature of Each Component")
    saveplot("temps", plt, si.plotdir)


def plot_temps_separately(x, y, si):
    colors=color_list()
    for num, comp in enumerate(si.components):
        idx = 1 + si.ne._npg + si.ne._ndg + num
        plt.plot(x, y[:, idx], label=comp.name, marker='.',color=colors[num % len(colors)])
        plt.xlabel("Time [s]")
        plt.ylabel("Temperature [K]")
        plt.title("Temperature of " + comp.name)
        plt.legend()
        saveplot(comp.name + " Temp[K]", plt, si.plotdir)


def plot_zetas(x, y, si):
    for num in range(0, si.ne._npg):
        idx = num + 1
        plt.plot(x, y[:, idx], marker='.', label="i = " + str(idx))
    plt.xlabel(r'Time $[s]$')
    plt.ylabel(r"Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    plt.title(r"Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    plt.legend()
    saveplot("zetas", plt, si.plotdir)


def plot_omegas(x, y, si):
    for num in range(0, si.ne._ndg):
        idx = 1 + si.ne._npg + num
        plt.plot(x, y[:, idx], marker='.', label="i = " + str(idx))
    plt.legend()
    plt.xlabel(r'Time $[s]$')
    plt.ylabel(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
    plt.title(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
    saveplot("omegas", plt, si.plotdir)


def saveplot(name, plt, plotdir='images'):
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    plt.savefig(str(plotdir + "/" + name + '.pdf'), bbox_inches='tight')
    plt.savefig(str(plotdir + "/" + name + '.eps'), bbox_inches='tight')
    plt.clf()
