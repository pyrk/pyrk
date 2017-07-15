from nose.tools import assert_equal, assert_raises

from pyrk.inp import validation as v
from pyrk.utilities.ur import units


def test_ge_wrong_type():
    val = "ten"
    valname = "testval"
    llim = 0
    assert_raises(TypeError, v.validate_ge, valname, val, llim)


def test_ge_Quantity_type():
    val = 10*units.meter
    valname = "testval"
    llim = 0*units.meter
    assert_equal(v.validate_ge(valname, val, llim), val)


def test_ge_right_type():
    val = 10
    valname = "testval"
    llim = 0
    assert_equal(v.validate_ge(valname, val, llim), val)


def test_ge_too_small():
    val = -2
    valname = "testval"
    llim = 0
    assert_raises(ValueError, v.validate_ge, valname, val, llim)


def test_ge_both_neg():
    val = -2
    valname = "testval"
    llim = -3
    assert_equal(v.validate_ge(valname, val, llim), val)


def test_le_wrong_type():
    val = "ten"
    valname = "testval"
    ulim = 20
    assert_raises(TypeError, v.validate_le, valname, val, ulim)


def test_le_right_type():
    val = 1
    valname = "testval"
    ulim = 10
    assert_equal(v.validate_le(valname, val, ulim), val)


def test_le_too_big():
    val = 2
    valname = "testval"
    ulim = 0
    assert_raises(ValueError, v.validate_le, valname, val, ulim)


def test_le_both_large():
    val = 1000000000000000
    valname = "testval"
    ulim = val
    assert_equal(v.validate_le(valname, val, ulim), val)


def test_num_Quantity_type():
    val = 10*units.meter
    valname = "testval"
    assert_equal(v.validate_num(valname, val), val)
