from pyrk import neutronics


def test_default_constructor():
    ne = neutronics.Neutronics()
    assert ne._iso == "u235"
    assert ne._e == "thermal"
    assert ne._npg == 6
    assert ne._ndg == 11


def test_malformed_constructor():
    assert_raises(ValueError, neutronics.Neutronics, iso="th233")
    assert_raises(ValueError, neutronics.Neutronics, e="epithermal")
    assert_raises(ValueError, neutronics.Neutronics, n_precursors=99)
    assert_raises(ValueError, neutronics.Neutronics, n_decay=99)
