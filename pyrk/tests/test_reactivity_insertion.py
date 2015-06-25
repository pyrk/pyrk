from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import reactivity_insertion as ri
import timer
from ur import units

ti = timer.Timer(t0=0.0*units.seconds,
                 tf=10.0*units.seconds,
                 dt=0.01*units.seconds)


def test_default_ri():
    default = ri.ReactivityInsertion(timer=ti)
    assert_equal(default.reactivity(0), 0.0*units.delta_k)
    assert_equal(default.reactivity(1), 0.0*units.delta_k)
    assert_equal(default.reactivity(10), 0.0*units.delta_k)
    assert_equal(default.reactivity(1000), 0.0*units.delta_k)


def test_default_step_ri():
    step = ri.StepReactivityInsertion(timer=ti)
    assert_equal(step.t_step, 1.0*units.seconds)
    assert_equal(step.reactivity(0), 0.0*units.delta_k)
    assert_equal(step.reactivity(1), 0.0*units.delta_k)
    assert_equal(step.reactivity(101), 1.0*units.delta_k)
    assert_equal(step.reactivity(1000), 1.0*units.delta_k)


def test_custom_step_ri():
    t_step = 2.0*units.seconds
    rho_init = 1.0*units.delta_k
    rho_final = 2.0*units.delta_k
    t_step_idx = ti.t_idx(t_step)
    step = ri.StepReactivityInsertion(timer=ti,
                                      t_step=t_step,
                                      rho_init=rho_init,
                                      rho_final=rho_final)
    assert_equal(step.reactivity(0), rho_init)
    assert_equal(step.reactivity(1), rho_init)
    assert_equal(step.reactivity(t_step_idx + 1), rho_final)
    assert_equal(step.reactivity(1000), rho_final)


def test_default_impulse_ri():
    impulse = ri.ImpulseReactivityInsertion(timer=ti)
    assert_equal(impulse.reactivity(0), 0.0*units.delta_k)
    assert_equal(impulse.reactivity(1), 0.0*units.delta_k)
    assert_equal(impulse.reactivity(101), 1.0*units.delta_k)
    assert_equal(impulse.reactivity(1000), 0.0*units.delta_k)


def test_custom_impulse_ri():
    t_start = 2.0*units.seconds
    t_end = 3.0*units.seconds
    rho_init = 1.0*units.delta_k
    rho_max = 2.0*units.delta_k
    t_start_idx = ti.t_idx(t_start)
    t_end_idx = ti.t_idx(t_end)
    impulse = ri.ImpulseReactivityInsertion(timer=ti,
                                            t_start=t_start,
                                            t_end=t_end,
                                            rho_init=rho_init,
                                            rho_max=rho_max)
    assert_equal(impulse.reactivity(0), rho_init)
    assert_equal(impulse.reactivity(1), rho_init)
    assert_equal(impulse.reactivity(t_start_idx + 1), rho_max)
    assert_equal(impulse.reactivity(t_end_idx + 1), rho_init)
    assert_equal(impulse.reactivity(1000), rho_init)


def test_default_ramp_ri():
    ramp = ri.RampReactivityInsertion(timer=ti)
    assert_equal(ramp.reactivity(0), 0.0*units.delta_k)
    assert_equal(ramp.reactivity(1), 0.0*units.delta_k)
    assert_true(ramp.reactivity(101) > 0.0*units.delta_k)
    assert_true(ramp.reactivity(101) < 1.0*units.delta_k)
    assert_equal(ramp.reactivity(1000), 1.0*units.delta_k)


def test_custom_ramp_ri():
    t_start = 2.0*units.seconds
    t_end = 3.0*units.seconds
    rho_init = 1.0*units.delta_k
    rho_rise = 2.0*units.delta_k
    rho_final = 1.5*units.delta_k
    t_start_idx = ti.t_idx(t_start)
    t_end_idx = ti.t_idx(t_end)
    ramp = ri.RampReactivityInsertion(timer=ti,
                                      t_start=t_start,
                                      t_end=t_end,
                                      rho_init=rho_init,
                                      rho_rise=rho_rise,
                                      rho_final=rho_final)
    assert_equal(ramp.reactivity(0), rho_init)
    assert_equal(ramp.reactivity(1), rho_init)
    assert_true(ramp.reactivity(t_start_idx + 1) > rho_init)
    assert_true(ramp.reactivity(t_start_idx + 1) < rho_init+rho_rise)
    assert_equal(ramp.reactivity(t_end_idx + 1), rho_final)
    assert_equal(ramp.reactivity(1000), rho_final)
