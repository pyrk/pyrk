from nose.tools import assert_equal

from pyrk.materials import graphite
from pyrk.utilities.ur import units
from pyrk.timer import Timer

name = "testname"
kappa = 0
T0 = 700 * units.kelvin
t0 = 0 * units.seconds
tf = 10 * units.seconds
dt = 0.1 * units.seconds
ti = Timer(t0=t0, tf=tf, dt=dt)
tester = graphite.Graphite(name=name)

k_graphite = 0.26 * units.watt / (units.meter * units.kelvin)
cp_graphite = 1650.0 * units.joule / (units.kg * units.kelvin)
rho_const = 1740. * units.kg / (units.meter**3)


def test_constructor():
    assert_equal(tester.name, name)
    assert_equal(tester.k, k_graphite)
    assert_equal(tester.cp, cp_graphite)
    assert_equal(tester.rho(temp=0 * units.kelvin), rho_const)


def test_temp():
    assert_equal(tester.rho(temp=0 * units.kelvin), rho_const)
    assert_equal(tester.rho(temp=T0), rho_const)
