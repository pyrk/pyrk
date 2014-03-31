import numpy as np

import neutronics 
import thermal_hydraulics
from scipy.integrate import ode

np.set_printoptions(precision=3)
t0 = 0.0000
dt = 0.0001
tf = 0.002
timesteps = tf/dt + 2

n_precursor_groups = 6
n_decay_groups = 3
n_components = len(component_names)
n_entries = 1 + n_precursor_groups + n_decay_groups + n_components

coeffs = {"fuel":-3.8, "cool":-1.8, "mod":-0.7, "refl":1.8}

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

ne = neutronics.Neutronics()
th = thermal_hydraulics.ThermalHydraulics()
component_names = th._params._components
for key, val in th._params._init_temps.iteritems():
    _temp[0][component_names[key]] = val  

def update_n(t, y_n):
    n_n = len(y_n)
    _y[t/dt][:n_n] = y_n

def update_th(t, y_n, y_th):
    _temp[int(t/dt)] = y_th
    n_n = len(y_n)
    _y[t/dt][n_n:] = y_th

def f_n(t, y, coeffs):
    lams = ne._data._lambdas
    f = {"p":ne.dpdt(t, dt, _temp, coeffs, y[0],
        y[1:n_precursor_groups+1])}
    #print str(f)
    for j in range(0, n_precursor_groups):
        name = "ksi"+str(j)
        f[name] = ne.dksidt(t, y[0], y[j+1], j)
    #print str(f)
    for k in range(0, n_decay_groups):
        name = "w"+str(k)
        f[name] = ne.dwdt(y[0], k)
    #print str(f)
    #print "type of f_n : "+ str(type(f.values()))
    #print "len of f_n : "+ str(len(f.values()))
    return f.values()

def f_th(t, y_th):
    f = {}
    power = _y[t/dt][0]
    o_i = 1+n_precursor_groups
    o_f = 1+n_precursor_groups+n_decay_groups
    omegas = _y[t/dt][o_i:o_f]
    for c in component_names:
        f[c] = th.dtempdt(c, y_th, power, omegas, component_names)
    #print "type of f_th : "+ str(type(f.values()))
    return f.values()

def y0(): 
    y0 = [1] # real power is 236 MWth, but normalized is 1
    for j in range(0, n_precursor_groups):
        y0.append(0)
    for k in range(0, n_decay_groups):
        y0.append(ne._data._omegas[k])
    for name, num in component_names.iteritems():
        y0.append(th.temp(name, 0))
    assert len(y0) == n_entries
    _y[0] = y0
    return y0

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
        print("NT: ", n.t)
        print "NE result:"
        print(n.t, n.y)
        update_n(n.t, n.y)
        th.integrate(th.t+dt)
        print "TH result:"
        print(th.t, th.y)
        update_th(n.t, n.y, th.y)
    print("Final Result : ", _y) 
    print("Final Temps :",_temp)
    print(ne._data._lambdas)
    print(ne._data._betas)
