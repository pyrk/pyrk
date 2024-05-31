import pyrk.reactivity_insertion as ri
from pyrk import timer
from pyrk.utilities.ur import units

ti = timer.Timer(t0=0.0 * units.seconds,
                 tf=10.0 * units.seconds,
                 dt=0.01 * units.seconds)


def test_default_ri():
    default = ri.ReactivityInsertion(timer=ti)
    assert default.reactivity(0) == 0.0 * units.delta_k
    assert default.reactivity(1) == 0.0 * units.delta_k
    assert default.reactivity(10) == 0.0 * units.delta_k
    assert default.reactivity(1000) == 0.0 * units.delta_k


def test_default_step_ri():
    step = ri.StepReactivityInsertion(timer=ti)
    assert step.t_step == 1.0 * units.seconds
    assert step.reactivity(0) == 0.0 * units.delta_k
    assert step.reactivity(1) == 0.0 * units.delta_k
    assert step.reactivity(101) == 1.0 * units.delta_k
    assert step.reactivity(1000) == 1.0 * units.delta_k


def test_custom_step_ri():
    t_step = 2.0 * units.seconds
    rho_init = 1.0 * units.delta_k
    rho_final = 2.0 * units.delta_k
    t_step_idx = ti.t_idx(t_step)
    step = ri.StepReactivityInsertion(timer=ti,
                                      t_step=t_step,
                                      rho_init=rho_init,
                                      rho_final=rho_final)
    assert step.reactivity(0) == rho_init
    assert step.reactivity(1) == rho_init
    assert step.reactivity(t_step_idx + 1) == rho_final
    assert step.reactivity(1000) == rho_final


def test_default_impulse_ri():
    impulse = ri.ImpulseReactivityInsertion(timer=ti)
    assert impulse.reactivity(0) == 0.0 * units.delta_k
    assert impulse.reactivity(1) == 0.0 * units.delta_k
    assert impulse.reactivity(101) == 1.0 * units.delta_k
    assert impulse.reactivity(1000) == 0.0 * units.delta_k


def test_custom_impulse_ri():
    t_start = 2.0 * units.seconds
    t_end = 3.0 * units.seconds
    rho_init = 1.0 * units.delta_k
    rho_max = 2.0 * units.delta_k
    t_start_idx = ti.t_idx(t_start)
    t_end_idx = ti.t_idx(t_end)
    impulse = ri.ImpulseReactivityInsertion(timer=ti,
                                            t_start=t_start,
                                            t_end=t_end,
                                            rho_init=rho_init,
                                            rho_max=rho_max)
    assert impulse.reactivity(0) == rho_init
    assert impulse.reactivity(1) == rho_init
    assert impulse.reactivity(t_start_idx + 1) == rho_max
    assert impulse.reactivity(t_end_idx + 1) == rho_init
    assert impulse.reactivity(1000) == rho_init


def test_default_ramp_ri():
    ramp = ri.RampReactivityInsertion(timer=ti)
    assert ramp.reactivity(0) == 0.0 * units.delta_k
    assert ramp.reactivity(1) == 0.0 * units.delta_k
    assert ramp.reactivity(101) > 0.0 * units.delta_k
    assert ramp.reactivity(101) < 1.0 * units.delta_k
    assert ramp.reactivity(1000) == 1.0 * units.delta_k


def test_custom_ramp_ri():
    t_start = 2.0 * units.seconds
    t_end = 3.0 * units.seconds
    rho_init = 1.0 * units.delta_k
    rho_rise = 2.0 * units.delta_k
    rho_final = 1.5 * units.delta_k
    t_start_idx = ti.t_idx(t_start)
    t_end_idx = ti.t_idx(t_end)
    ramp = ri.RampReactivityInsertion(timer=ti,
                                      t_start=t_start,
                                      t_end=t_end,
                                      rho_init=rho_init,
                                      rho_rise=rho_rise,
                                      rho_final=rho_final)
    assert ramp.reactivity(0) == rho_init
    assert ramp.reactivity(1) == rho_init
    assert ramp.reactivity(t_start_idx + 1) > rho_init
    assert ramp.reactivity(t_start_idx + 1) < rho_init + rho_rise
    assert ramp.reactivity(t_end_idx + 1) == rho_final
    assert ramp.reactivity(1000) == rho_final
