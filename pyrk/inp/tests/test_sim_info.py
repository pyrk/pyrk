from nose.tools import assert_equal, assert_false, with_setup

import os

from pyrk.inp import sim_info as si
from pyrk.db import database

from pyrk.utilities.ur import units
from pyrk import th_component
from pyrk.timer import Timer


def setup_func():
    "set up test fixtures"
    file = open('testfile.py', 'w+')
    file.close()


def teardown_func():
    "tear down test fixtures"
    os.remove('testfile.py')


@with_setup(setup_func, teardown_func)
def test_init_reasonable_sim_no_components():
    t0 = 0 * units.seconds
    tf = 10 * units.seconds
    t_feedback = 1. * units.seconds
    dt = 0.1 * units.seconds
    ti = Timer(t0=t0, tf=tf, t_feedback=t_feedback, dt=dt)
    iso = "u235"
    spectrum = "thermal"
    npg = 6
    ndg = 11
    kappa = 0.06
    kappa = 0.0
    testfile = 'testfile.py'
    open(testfile, 'w+')
    info = si.SimInfo(timer=ti,
                      components={},
                      iso=iso,
                      e=spectrum,
                      n_precursors=npg,
                      n_decay=ndg,
                      kappa=kappa,
                      infile=testfile,
                      sim_id=None,
                      db=database.Database(mode='w'))
    assert_equal(t0, info.timer.t0)
    assert_equal(tf, info.timer.tf)
    assert_equal(dt, info.timer.dt)
    assert_equal(info.timer.timesteps(), 101)
    info.db.close_db()
    info.db.delete_db()


@with_setup(setup_func, teardown_func)
def test_init_reasonable_sim_w_components():
    t0 = 0 * units.seconds
    tf = 10 * units.seconds
    t_feedback = 1. * units.seconds
    dt = 0.1 * units.seconds
    ti = Timer(t0=t0, tf=tf, t_feedback=t_feedback, dt=dt)
    iso = "u235"
    spectrum = "thermal"
    npg = 6
    ndg = 11
    kappa = 0.06
    tester = th_component.THComponent()
    c = [tester, tester, tester]
    kappa = 0.0
    testfile = 'testfile.py'
    open(testfile, 'w+')
    info = si.SimInfo(timer=ti, components=c, iso=iso, e=spectrum,
                      n_precursors=npg, n_decay=ndg, kappa=kappa,
                      infile=testfile, db=database.Database(mode='w'))
    assert_equal(t0, info.timer.t0)
    assert_equal(tf, info.timer.tf)
    assert_equal(dt, info.timer.dt)
    assert_equal(info.timer.timesteps(), 101)
    info.db.close_db()
    info.db.delete_db()


def test_sim_id():
    info = si.SimInfo()
    first_id = info.generate_sim_id()
    next_id = info.generate_sim_id()
    assert_false(first_id == next_id)
    info.db.close_db()
    info.db.delete_db()
