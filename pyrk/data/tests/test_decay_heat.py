from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from data import decay_heat



def test_u235_thermal_constructor():
    n = 11
    nuc = "u235"
    e = "thermal"
    d = decay_heat.DecayData(nuc=nuc, e=e, n=n)


def test_u235_fast_constructor():
    assert_false(False)


def test_pu239_thermal_constructor():
    assert_false(False)


def test_pu239_fast_constructor():
    assert_false(False)
