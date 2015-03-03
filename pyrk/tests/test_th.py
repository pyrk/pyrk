from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import th
from inp import sim_info



def test_constructor():
    name = "testname"
    vol = 20
    k = 10
    rho = 100
    T0 = 700
    si = sim_info.SimInfo(t0=0, tf=10, dt=0.1)
    tester = th.THComponent(name, vol, k, rho, T0, si)
    assert_equal(tester.name, name)
    assert_equal(tester.vol, vol)
    assert_equal(tester.k, k)
    assert_equal(tester.rho, rho)
    assert_equal(tester.T0, T0)
