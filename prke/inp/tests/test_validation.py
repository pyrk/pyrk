from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from prke.inp import validation as v


def test_validation_ge_wrong_type():
    val = "ten"
    valname = "testval"
    llim = 0
    assert_raises(TypeError, v.validate_ge, valname, val, llim)


def test_validation_ge_right_type():
    val = 10
    valname = "testval"
    llim = 0
    assert_equal(v.validate_ge(valname, val, llim), 10)


def test_validation_ge_too_small():
    val = -2
    valname = "testval"
    llim = 0
    assert_raises(ValueError, v.validate_ge, valname, val, llim)


def test_validation_ge_both_neg():
    val = -2
    valname = "testval"
    llim = -3
    assert_equal(v.validate_ge(valname, val, llim), -2)
