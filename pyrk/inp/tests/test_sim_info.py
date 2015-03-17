from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from pyrk.inp import sim_info as si

from ur import units


def test_init_reasonable_sim():
    t0 = 0*units.seconds
    tf = 10*units.seconds
    dt = 0.1*units.seconds
    info = si.SimInfo(t0, tf, dt)
    assert_equal(t0, info.t0)
    assert_equal(tf, info.tf)
    assert_equal(t0, info.t0)
    assert_equal(info.timesteps(),101)
