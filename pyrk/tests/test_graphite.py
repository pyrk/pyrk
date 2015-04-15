from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import graphite
from inp import sim_info
from ur import units
from timer import Timer

name = "testname"
vol = 20*units.meter**3
kappa = 0
T0 = 700*units.kelvin
t0 = 0*units.seconds
tf = 10*units.seconds
dt = 0.1*units.seconds
ti = Timer(t0=t0, tf=tf, dt=dt)
tester = graphite.Graphite(name=name, vol=vol, T0=T0, timer=ti)
si = sim_info.SimInfo(kappa=kappa, timer=ti)

k_graphite = 0.26*units.watt/(units.meter*units.kelvin)
cp_graphite = 1650.0*units.joule/(units.kg*units.kelvin)
rho_const = 1740.*units.kg/(units.meter**3)


def test_constructor():
    assert_equal(tester.name, name)
    assert_equal(tester.vol, vol)
    assert_equal(tester.k, k_graphite)
    assert_equal(tester.cp, cp_graphite)
    assert_equal(tester.rho(timestep=0), rho_const)
    assert_equal(tester.T0, T0)


def test_temp():
    assert_equal(tester.temp(0), T0)


def test_update_temp():
    assert_equal(tester.temp(0), T0)
    T1 = 10*units.kelvin
    T2 = 20*units.kelvin
    tester.update_temp(1, T1)
    assert_equal(tester.temp(1), T1)
    tester.update_temp(2, T2)
    assert_equal(tester.temp(2), T2)
