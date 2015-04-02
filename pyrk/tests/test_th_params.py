from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import th_params
from ur import units

components = {"fuel": 0, "cool": 1, "mod": 2, "refl": 3}


def test_h():
    uh = units.watt/units.kelvin/units.meter**2
    d = th_params.THParams()
    obs = d.h(set(["cool", "fuel"]))
    assert_true(obs > 0*uh)
    obs = d.h(set(["fuel", "cool"]))
    assert_true(obs > 0*uh)
    obs = d.h(set(["cool", "refl"]))
    assert_true(obs > 0*uh)
    obs = d.h(set(["refl", "cool"]))
    assert_true(obs > 0*uh)

    assert_raises(KeyError, d.h, set(["bob", "refl"]))


def test_cp():
    d = th_params.THParams()
    obs = d.cp("mod")
    assert_true(obs.magnitude > 0)
    obs = d.cp("fuel")
    assert_true(obs.magnitude > 0)
    obs = d.cp("cool")
    assert_true(obs.magnitude > 0)
    obs = d.cp("refl")
    assert_raises(KeyError, d.cp, "bob")


def test_res_conv():
    ures = units.kelvin/units.watt
    d = th_params.THParams()
    obs = d.res_conv("cool", "fuel")
    assert_true(obs > 0*ures)
    obs = d.res_conv("fuel", "cool")
    assert_true(obs > 0*ures)
    obs = d.res_conv("refl", "cool")
    assert_true(obs > 0*ures)
    obs = d.res_conv("cool", "refl")
    assert_true(obs > 0*ures)
    assert_raises(KeyError, d.res_conv, "bob", "refl")


def test_res_cond():
    ures = units.kelvin/units.watt
    d = th_params.THParams()
    obs = d.res_cond("mod", "fuel")
    assert_true(obs > 0*ures)
    obs = d.res_cond("fuel", "mod")
    assert_true(obs > 0*ures)
    assert_raises(KeyError, d.res_cond, "bob", "refl")


def test_rho():
    urho = units.kg/units.meter**3
    d = th_params.THParams()
    T = 750.0*units.kelvin
    obs = d.rho("mod", T)
    assert_true(obs > 0*urho)
    obs = d.rho("fuel", T)
    assert_true(obs > 0*urho)
    obs = d.rho("cool", T)
    assert_true(obs > 0*urho)
    obs = d.rho("fuel", T)
    assert_true(obs > 0*urho)
    obs = d.rho("refl", T)
    assert_true(obs > 0*urho)
    obs = d.rho("cool", T)
    assert_true(obs > 0*urho)
    assert_raises(KeyError, d.rho, "bob", T)
