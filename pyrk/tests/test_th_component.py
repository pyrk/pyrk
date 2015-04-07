from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import th_system
import th_component as th
from inp import sim_info
import density_model
from ur import units


name = "testname"
vol = 20*units.meter**3
k = 10*units.watt/units.meter/units.kelvin
cp = 10*units.joule/units.kg/units.kelvin
dm = density_model.DensityModel(a=0*units.kg/units.meter**3,
                                b=100*units.kg/units.meter**3,
                                model='constant')
T0 = 700*units.kelvin
si = sim_info.SimInfo(t0=0*units.seconds, tf=10*units.seconds,
                      dt=0.1*units.seconds,
                      th=th_system.THSystem())
tester = th.THComponent(name, vol, k, cp, dm, T0, si.timesteps())


def test_constructor():
    assert_equal(tester.name, name)
    assert_equal(tester.vol, vol)
    assert_equal(tester.k, k)
    assert_equal(tester.rho(0), dm.rho())
    assert_equal(tester.T0, T0)


def test_temp():
    assert_equal(tester.temp(0), T0)


def test_update_temp():
    assert_equal(tester.temp(0), T0)
    T1 = 10*units.kelvin
    T2 = 20*units.kelvin
    tester.update_temp(1, T1)
    assert_equal(tester.temp(1), T0+T1)
    tester.update_temp(2, T2)
    assert_equal(tester.temp(2), T0+T1+T2)
