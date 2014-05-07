from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import numpy as np
import th_params


components = {"fuel":0,"cool":1,"mod":2,"refl":3}

def test_res():
    d = th_params.THParams()
    for c, val in components.iteritems():
        obs = d.h(set([c]))
        assert_true(obs>0)

def test_cp():
    d = th_params.THParams()
    obs = d.cp("mod")
    assert_true(obs > 0)
    obs = d.cp("fuel")
    assert_true(obs > 0)
    obs = d.cp("cool")
    assert_true(obs > 0)
    obs = d.cp("refl")
    assert_raises(KeyError, d.cp, "bob")

def test_res():
    d = th_params.THParams()
    obs = d.res("mod", "fuel")
    assert_true(obs > 0)
    obs = d.res("fuel", "mod")
    assert_true(obs > 0)
    obs = d.res("cool", "fuel")
    assert_true(obs > 0)
    obs = d.res("fuel", "cool")
    assert_true(obs > 0)
    obs = d.res("refl", "cool")
    assert_true(obs > 0)
    obs = d.res("cool", "refl")
    assert_true(obs > 0)
    assert_raises(KeyError, d.res, "bob", "refl")


def test_rho():
    d = th_params.THParams()
    obs = d.rho("mod", 750.)
    assert_true(obs > 0)
    obs = d.rho("fuel", 750.)
    assert_true(obs > 0)
    obs = d.rho("cool", 750.)
    assert_true(obs > 0)
    obs = d.rho("fuel", 750.)
    assert_true(obs > 0)
    obs = d.rho("refl", 750.)
    assert_true(obs > 0)
    obs = d.rho("cool", 750.)
    assert_true(obs > 0)
    assert_raises(KeyError, d.rho, "bob", 750.)
