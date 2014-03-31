import numpy as np

import neutronics 
import thermal_hydraulics
from scipy.integrate import ode

np.set_printoptions(precision=3)
t0 = 0.0
dt = 0.0001
tf = 0.0004
timesteps = tf/dt + 1

n_precursor_groups = 6
n_decay_groups = 3
component_names = {"fuel":0, "cool":1, "mod":2, "refl":3}
n_components = len(component_names)
n_entries = 1 + n_precursor_groups + n_decay_groups + n_components

coeffs = {"fuel":-3.8, "cool":-1.8, "mod":-0.7, "refl":1.8}

y = np.zeros(shape = (timesteps, n_entries), dtype=float)
#dydt = np.zeros(shape = (timesteps, n_entries), dtype=float)

#p = np.zeros(shape= (1, timesteps), dtype=float)
#dpdt = np.zeros(shape= (1, timesteps), dtype=float)

#ksi = np.zeros(shape= (n_precursor_groups, timesteps), dtype=float)
#dksidt = np.zeros(shape= (n_precursor_groups, timesteps), dtype=float)

#w = np.zeros(shape= (n_decay_groups, timesteps), dtype=float)
#dwdt = np.zeros(shape= (n_decay_groups, timesteps), dtype=float)

temp = np.zeros(shape= (timesteps, n_components), dtype=float)
#dtempdt = np.zeros(shape= (n_components, timesteps), dtype=float)

ne = neutronics.Neutronics()
th = thermal_hydraulics.ThermalHydraulics()

def update_n(t, y_n):
    n_n = len(y_n)
    y[t][:n_n] = y_n

def update_th(t, y_n, y_th):
    temp[t] = y_th
    n_n = len(y_n)
    y[t][n_n:] = y_th

def f_n(t, y, coeffs):
    lams = ne._data._lambdas
    f = {"p":ne.dpdt(t, dt, temp, coeffs, y[0],
        y[1:n_precursor_groups+1])}
    #print str(f)
    for j in range(0, n_precursor_groups):
        name = "ksi"+str(j)
        f[name] = ne.dksidt(t, y[0], y[j+1], j)
    #print str(f)
    for k in range(0, n_decay_groups):
        name = "w"+str(k)
        f[name] = ne.dwdt(k)
    #print str(f)
    #print "type of f_n : "+ str(type(f.values()))
    #print "len of f_n : "+ str(len(f.values()))
    return f.values()

def f_th(t, y_th):
    f = {}
    power = y[t][0]
    o_i = 1+n_precursor_groups
    o_f = 1+n_precursor_groups+n_decay_groups
    omegas = y[t][o_i:o_f]
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
    y[0] = y0
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
        print "NE result:"
        print(n.t, n.y)
        update_n(int(n.t/dt), n.y)
        th.integrate(th.t+dt)
        print "TH result:"
        print(th.t, th.y)
        update_th(int(n.t/dt), n.y, th.y)
    print("Final Result : ", y) 

