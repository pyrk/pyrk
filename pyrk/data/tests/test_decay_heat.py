from nose.tools import assert_equal

from pyrk.data import decay_heat


def test_u235_thermal_constructor():
    n = 11
    nuc = "u235"
    e = "thermal"
    d = decay_heat.DecayData(nuc=nuc, e=e, n=n)
    assert_equal(d._n, n)
    assert_equal(d._e, e)
    assert_equal(d._nuc, nuc)
    assert_equal(len(d._lambdas), n)
    assert_equal(d._lambdas, d.lambdas())
    assert_equal(d._kappas, d.kappas())


def test_u235_fast_constructor():
    n = 11
    nuc = "u235"
    e = "fast"
    d = decay_heat.DecayData(nuc=nuc, e=e, n=n)
    assert_equal(d._n, n)
    assert_equal(d._e, e)
    assert_equal(d._nuc, nuc)


def test_pu239_thermal_constructor():
    # TODO This should actually test for a warning to be issued
    n = 11
    nuc = "pu239"
    e = "thermal"
    d = decay_heat.DecayData(nuc=nuc, e=e, n=n)
    assert_equal(d._n, n)
    assert_equal(d._e, e)
    assert_equal(d._nuc, nuc)


def test_pu239_fast_constructor():
    # TODO This should actually test for a warning to be issued
    n = 11
    nuc = "pu239"
    e = "fast"
    d = decay_heat.DecayData(nuc=nuc, e=e, n=n)
    assert_equal(d._n, n)
    assert_equal(d._e, e)
    assert_equal(d._nuc, nuc)
