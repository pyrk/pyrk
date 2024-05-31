import pytest
from pyrk.inp import validation as v
from pyrk.utilities.ur import units


def test_ge_wrong_type():
    with pytest.raises(TypeError) as excinfo:
        val = "ten"
        valname = "testval"
        llim = 0
        v.validate_ge(valname, val, llim)
    assert excinfo.value == TypeError


def test_ge_Quantity_type():
    val = 10 * units.meter
    valname = "testval"
    llim = 0 * units.meter
    assert v.validate_ge(valname, val, llim) == val


def test_ge_right_type():
    val = 10
    valname = "testval"
    llim = 0
    assert v.validate_ge(valname, val, llim) == val


def test_ge_too_small():
    with pytest.raises(ValueError) as excinfo:
        val = -2
        valname = "testval"
        llim = 0
        v.validate_ge(valname, val, llim)
    assert excinfo.value == ValueError


def test_ge_both_neg():
    val = -2
    valname = "testval"
    llim = -3
    assert v.validate_ge(valname, val, llim) == val


def test_le_wrong_type():
    with pytest.raises(TypeError) as excinfo:
        val = "ten"
        valname = "testval"
        ulim = 20
        v.validate_le(valname, val, ulim)
    assert excinfo.value == TypeError


def test_le_right_type():
    val = 1
    valname = "testval"
    ulim = 10
    assert v.validate_le(valname, val, ulim) == val


def test_le_too_big():
    with pytest.raises(ValueError) as excinfo:
        val = 2
        valname = "testval"
        ulim = 0
        v.validate_le(valname, val, ulim)
    assert excinfo.value == ValueError


def test_le_both_large():
    val = 1000000000000000
    valname = "testval"
    ulim = val
    assert v.validate_le(valname, val, ulim) == val


def test_num_Quantity_type():
    val = 10 * units.meter
    valname = "testval"
    assert v.validate_num(valname, val) == val
