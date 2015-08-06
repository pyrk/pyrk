# Licensed under a 3-clause BSD-style license - see LiCENSE.rst
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors


def my_colors(num, n):
    """Returns a nice looking color map"""
    values = range(n)
    jet = plt.get_cmap('jet')
    c_norm = colors.Normalize(vmin=0, vmax=values[-1])
    scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=jet)
    color_val = scalar_map.to_rgba(values[num])
    return color_val


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
    plt.plot(x, si.ne._rho, color=my_colors(1, len(si.ne._rho)),
             marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Reactivity [$\Delta k/k$]")
    plt.title("Reactivity [$\Delta k/k$]")
    saveplot("reactivity", plt, si.plotdir)


def plot_power(x, y, si):
    power = y[:, 0]
    plt.plot(x, power, color=my_colors(1, len(y)), marker='.')
    plt.xlabel("Time [s]")
    plt.ylabel("Power [units]")
    plt.title("Power [units]")
    saveplot("power", plt, si.plotdir)


def plot_power_w_reactivity(x, si, y):
    power = y[:, 0]
    rho = si.ne._rho
    plt.plot(x, power, color=my_colors(0, 2), marker='.', label="Power")
    plt.plot(x, rho, color=my_colors(1, 2), marker='.',
             label="External Reactivity")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Power and Reactivity [$\Delta k$]")
    plt.title("Power and Reactivity [$\Delta k$]")
    saveplot("pow_and_rho", plt, si.plotdir)


def plot_temps_together(x, y, si):
    for num, comp in enumerate(si.components):
        idx = 1 + si.ne._npg + si.ne._ndg + num
        plt.plot(x, y[:, idx], label=comp.name,
                 color=my_colors(num, len(si.components)), marker='.')
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature [K]")
    plt.title("Temperature of Each Component")
    saveplot("temps", plt, si.plotdir)


def plot_temps_separately(x, y, si):
    for num, comp in enumerate(si.components):
        idx = 1 + si.ne._npg + si.ne._ndg + num
        plt.plot(x, y[:, idx], label=comp.name,
                 color=my_colors(num, len(si.components)), marker='.')
        plt.xlabel("Time [s]")
        plt.ylabel("Temperature [K]")
        plt.title("Temperature of "+comp.name)
        plt.legend()
        saveplot(comp.name+" Temp[K]", plt, si.plotdir)


def plot_zetas(x, y, si):
    for num in range(0, si.ne._npg):
        idx = num + 1
        plt.plot(x, y[:, idx], color=my_colors(num, si.ne._npg), marker='.',
                 label="i = "+str(idx))
    plt.xlabel(r'Time $[s]$')
    plt.ylabel("Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    plt.title("Concentration of Neutron Precursors, $\zeta_i [\#/dr^3]$")
    plt.legend()
    saveplot("zetas", plt, si.plotdir)


def plot_omegas(x, y, si):
    for num in range(0, si.ne._ndg):
        idx = 1 + si.ne._npg + num
        plt.plot(x, y[:, idx], color=my_colors(num, si.ne._ndg), marker='.',
                 label="i = "+str(idx))
    plt.legend()
    plt.xlabel(r'Time $[s]$')
    plt.ylabel(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
    plt.title(r'Decay Heat Fractions, $\omega_i [\#/dr^3]$')
    saveplot("omegas", plt)


def saveplot(name, plt, plotdir='images'):
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)
    plt.savefig(str(plotdir+"/"+name+'.pdf'), bbox_inches='tight')
    plt.savefig(str(plotdir+"/"+name+'.eps'), bbox_inches='tight')
    plt.clf()
