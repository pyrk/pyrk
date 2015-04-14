from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

import neutronics


def test_default_constructor():
    ne = neutronics.Neutronics()
    assert_equal(ne._iso, "u235")
    assert_equal(ne._e, "thermal")
    assert_equal(ne._npg, 6)
    assert_equal(ne._ndg, 11)


def test_malformed_constructor():
    assert_raises(ValueError, neutronics.Neutronics, iso="th233")
    assert_raises(ValueError, neutronics.Neutronics, e="epithermal")
    assert_raises(ValueError, neutronics.Neutronics, n_precursors=99)
    assert_raises(ValueError, neutronics.Neutronics, n_decay=99)
