from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import th
from inp import sim_info
import density_model


name = "testname"
vol = 20
k = 10
dm = density_model.DensityModel(a=0, b=100, model='constant')
T0 = 700
si = sim_info.SimInfo(t0=0, tf=10, dt=0.1)
tester = th.THComponent(name, vol, k, dm, T0, si)


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
    tester.update_temp(1, 10)
    assert_equal(tester.temp(1), 10)
    tester.update_temp(2, 100)
    assert_equal(tester.temp(2), 100)
