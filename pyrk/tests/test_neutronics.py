from nose.tools import assert_equal, assert_raises

import pyrk.neutronics


def test_default_constructor():
    ne = pyrk.neutronics.Neutronics()
    assert_equal(ne._iso, "u235")
    assert_equal(ne._e, "thermal")
    assert_equal(ne._npg, 6)
    assert_equal(ne._ndg, 11)


def test_malformed_constructor():
    assert_raises(ValueError, pyrk.neutronics.Neutronics, iso="th233")
    assert_raises(ValueError, pyrk.neutronics.Neutronics, e="epithermal")
    assert_raises(ValueError, pyrk.neutronics.Neutronics, n_precursors=99)
    assert_raises(ValueError, pyrk.neutronics.Neutronics, n_decay=99)
