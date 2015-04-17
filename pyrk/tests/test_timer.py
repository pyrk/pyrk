from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from ur import units
import timer
import numpy as np


zero = 0.0*units.seconds
one = 1.0*units.seconds
ptone = 0.1*units.seconds
ten = 10.0*units.seconds
small = 0.0001*units.seconds
large = 1000.0*units.seconds

default = timer.Timer()
short_sim = timer.Timer(t0=zero,
                        tf=one,
                        dt=ptone)

long_sim = timer.Timer(t0=zero,
                       tf=large,
                       dt=small)
late_start = timer.Timer(t0=ten,
                         tf=large,
                         dt=small)
long_dt = timer.Timer(t0=zero,
                      tf=large,
                      dt=ten)

all_ints = timer.Timer(t0=0*units.seconds,
                       tf=10*units.seconds,
                       dt=1*units.seconds)

trouble = timer.Timer(t0=0.0*units.seconds,
                      tf=5.0*units.seconds,
                      dt=0.005*units.seconds)


def test_default_constructor():
    assert_equal(default.t0, 0.0*units.seconds)
    assert_equal(default.tf, 1.0*units.seconds)
    assert_equal(default.dt, 1.0*units.seconds)
    assert_equal(default.ts, 0)
    assert_equal(default.current_time(), 0.0*units.seconds)


def test_default_t_idx():
    assert_equal(default.t_idx(0.0*units.seconds), 0)
    assert_equal(default.t_idx(1.0*units.seconds), 1)
    assert_equal(default.timesteps(), 2)
    assert_equal(default.advance_time(1.0*units.seconds), 1.0*units.seconds)


def test_long_sim_t_idx():
    assert_equal(long_sim.t_idx(zero), 0)
    assert_equal(long_sim.t_idx(small), 1)
    assert_equal(long_sim.t_idx(large), long_sim.timesteps()-1)
    assert_equal(long_sim.timesteps(), large/small+1)
    for i in range(1, 5):
        assert_equal(long_sim.advance_time(i*small), i*small)
        assert_equal(long_sim.current_time(), i*small)


def test_all_ints_t_idx():
    assert_equal(all_ints.t_idx(zero), 0)
    assert_equal(all_ints.t_idx(one), 1)
    assert_equal(all_ints.t_idx(ten), all_ints.timesteps()-1)
    assert_equal(all_ints.timesteps(), 11)
    for i in range(1, 10):
        assert_equal(all_ints.advance_time(i*one), i*one)
        assert_equal(all_ints.current_time(), i*one)


def test_short_sim_t_idx():
    assert_equal(short_sim.t_idx(zero), 0)
    assert_equal(short_sim.t_idx(ptone), 1)
    assert_equal(short_sim.t_idx(one), short_sim.timesteps()-1)
    assert_equal(short_sim.timesteps(), one/ptone+1)
    for i in np.linspace(start=0, stop=1, num=11):
        t = i*units.seconds
        assert_equal(short_sim.advance_time(t), t)
        assert_equal(short_sim.current_time(), t)


def test_troublemaker():
    for i in range(0, 50):
        time = i*0.005*units.seconds
        assert_equal(trouble.t(trouble.t_idx(time)), time)
        assert_equal(trouble.advance_time(time), time)


def test_idx_from_t():
    dt = 0.005*units.seconds
    t0 = 0.0*units.seconds
    test_dict = {0.12*units.seconds: 24,
                 0.125*units.seconds: 25,
                 0.13*units.seconds: 26,
                 0.135*units.seconds: 27,
                 0.14*units.seconds: 28}
    for time, exp in test_dict.iteritems():
        obs = default.idx_from_t(time=time, t0=t0, dt=dt)
        assert_equal(obs, exp)


def test_idx_from_t_and_back():
    dt = 0.005*units.seconds
    t0 = 0.0*units.seconds
    test_dict = {0.12*units.seconds: 24,
                 0.125*units.seconds: 25,
                 0.13*units.seconds: 26,
                 0.135*units.seconds: 27,
                 0.14*units.seconds: 28}
    for time, exp in test_dict.iteritems():
        idx = trouble.idx_from_t(time=time, t0=t0, dt=dt)
        other_idx = trouble.idx_from_t(time=trouble.t(idx), t0=t0, dt=dt)
        assert_equal(idx, other_idx)
