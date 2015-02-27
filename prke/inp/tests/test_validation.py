from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from prke.inp import validation as v


def test_validation_ge_wrong_type():
    val = "ten"
    valname = "testval"
    llim = 0
    assert_raises(TypeError, v.validate_ge, [valname, val, llim])
