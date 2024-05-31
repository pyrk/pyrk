import pytest
from pyrk import neutronics


def test_default_constructor():
    ne = neutronics.Neutronics()
    assert ne._iso == "u235"
    assert ne._e == "thermal"
    assert ne._npg == 6
    assert ne._ndg == 11


def test_malformed_constructor():
    with pytest.raises(ValueError) as excinfo:
        neutronics.Neutronics(iso="th233")
    assert excinfo.type is ValueError
    with pytest.raises(ValueError) as excinfo:
        neutronics.Neutronics(e="epithermal")
    assert excinfo.type is ValueError
    with pytest.raises(ValueError) as excinfo:
        neutronics.Neutronics(n_precursor=99)
    assert excinfo.type is ValueError
    with pytest.raises(ValueError) as excinfo:
        neutronics.Neutronics(n_decay=99)
    assert excinfo.type is ValueError