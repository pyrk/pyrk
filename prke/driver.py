import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cmx 
import matplotlib.colors as colors
from matplotlib.pyplot import legend

from scipy.integrate import ode

import neutronics 
import thermal_hydraulics

np.set_printoptions(precision=5)
t0 = 0.0000
dt = 0.0002
tf = 0.001
timesteps = tf/dt + 1


coeffs = {"fuel":-3.8, "cool":-1.8, "mod":-0.7, "refl":1.8}

ne = neutronics.Neutronics()
th = thermal_hydraulics.ThermalHydraulics()
components = th._params._components
n_precursor_groups = 6
n_decay_groups = 3
n_components = len(components)
n_entries = 1 + n_precursor_groups + n_decay_groups + n_components

_y = np.zeros(shape = (timesteps, n_entries), dtype=float)

#dydt = np.zeros(shape = (timesteps, n_entries), dtype=float)

#p = np.zeros(shape= (1, timesteps), dtype=float)
#dpdt = np.zeros(shape= (1, timesteps), dtype=float)

#ksi = np.zeros(shape= (n_precursor_groups, timesteps), dtype=float)
#dksidt = np.zeros(shape= (n_precursor_groups, timesteps), dtype=float)

#w = np.zeros(shape= (n_decay_groups, timesteps), dtype=float)
#dwdt = np.zeros(shape= (n_decay_groups, timesteps), dtype=float)

_temp = np.zeros(shape= (timesteps, n_components), dtype=float)
#dtempdt = np.zeros(shape= (n_components, timesteps), dtype=float)

for key, val in th._params._init_temps.iteritems():
    _temp[0][components[key]] = val  

def update_n(t, y_n):
    n_n = len(y_n)
    _y[t/dt][:n_n] = y_n

def update_th(t, y_n, y_th):
    _temp[int(t/dt)][:] = y_th
    n_n = len(y_n)
    _y[t/dt][n_n:] = y_th

def f_n(t, y, coeffs):
    f = np.zeros(shape=(1+n_precursor_groups + n_decay_groups,), dtype=float)
    lams = ne._data._lambdas
    i=0
    f[i] = ne.dpdt(t, dt, _temp, coeffs, y[0], y[1:n_precursor_groups+1])
    #print str(f)
    for j in range(0, n_precursor_groups):
        i += 1
        f[i] = ne.dksidt(t, y[0], y[i], j)
    #print str(f)
    for k in range(0, n_decay_groups):
        i+=1
        f[i] = ne.dwdt(y[0], k)
    #print str(f)
    #print "type of f_n : "+ str(type(f.values()))
    #print "len of f_n : "+ str(len(f.values()))
    return f

def f_th(t, y_th):
    f = np.zeros(shape=(n_components,), dtype=float)
    power = _y[t/dt][0]
    o_i = 1+n_precursor_groups
    o_f = 1+n_precursor_groups+n_decay_groups
    omegas = _y[t/dt][o_i:o_f]
    for name, num in components.iteritems():
        f[num] = th.dtempdt(name, y_th, power, omegas, components)
    #print "type of f_th : "+ str(type(f.values()))
    return f

def y0(): 
    i = 0
    f = np.zeros(shape=(n_entries ,), dtype=float)
    f[i] = 1.0 # real power is 236 MWth, but normalized is 1
    for j in range(0, n_precursor_groups):
        i += 1
        f[i] = 0
    for k in range(0, n_decay_groups):
        i+=1
        f[i] = ne._data._omegas[k]
    for name, num in components.iteritems():
        f[i+num+1] = _temp[0][num]
    assert len(f) == n_entries
    _y[0] = f
    return f

def y0_n():
    idx = n_precursor_groups+n_decay_groups + 1
    #print "len y0_n : " + str(idx)
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
        #print("NT: ", n.t)
        #print "NE result:"
        #print(n.t, n.y)
        update_n(n.t, n.y)
        th.integrate(th.t+dt)
        #print "TH result:"
        #print(th.t, th.y)
        update_th(n.t, n.y, th.y)
    print("Final Result : ", _y) 
    print("Final Temps :",_temp)
    print(ne._data._lambdas)
    print(ne._data._betas)
    return _y

def my_colors(num):
    values = range(n_entries)
    jet = cm = plt.get_cmap('jet') 
    cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    colorVal = scalarMap.to_rgba(values[num])
    return colorVal

def plot(y):
    x=np.arange(t0,tf+dt,dt)
    plot_power(x, y)
    plot_ksis(x, y)
    plot_omegas(x, y)
    plot_temps_together(x, y)
    plot_temps_separately(x, y)

def plot_power(x, y):
    power = y[:,0]
    plt.plot(x, power, color=my_colors(1), marker='.')
    saveplot("power", plt)

def plot_temps_together(x, y):
    for name, num in components.iteritems():
        idx = 1 + n_precursor_groups + n_decay_groups + num
        plt.plot(x, y[:,idx],label=name, color=my_colors(num), marker='.')
    saveplot("temps", plt)

def plot_temps_separately(x, y):
    for name, num in components.iteritems():
        idx = 1 + n_precursor_groups + n_decay_groups + num
        plt.plot(x, y[:,idx],label=name, color=my_colors(num), marker='.')
        saveplot(name+" Temp[K]", plt)

def plot_ksis(x, y):
    for num in range(0, n_precursor_groups):
        idx = num + 1
        plt.plot(x, y[:,idx], color=my_colors(num), marker='.')
    saveplot("ksis", plt)

def plot_omegas(x, y):
    for num in range(0, n_decay_groups):
        idx = 1 + n_precursor_groups + num
        plt.plot(x, y[:,idx], color=my_colors(num), marker='.')
    saveplot("omegas", plt)

def saveplot(name, plt):
    plt.savefig(str(name+'.pdf'), bbox_inches='tight')
    plt.savefig(str(name+'.eps'), bbox_inches='tight')
    plt.clf()

