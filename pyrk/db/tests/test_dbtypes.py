from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup
import dbtypes
import tables as tb


def test_lookup_float():
    obs = dbtypes.pytables_type(float)
    exp = tb.Float64Col()
    assert_equal(obs, exp)


def test_lookup_int():
    obs = dbtypes.pytables_type(int)
    exp = tb.Int32Col()
    assert_equal(obs, exp)


def test_lookup_long():
    obs = dbtypes.pytables_type(long)
    exp = tb.Int64Col()
    assert_equal(obs, exp)


def test_lookup_str():
    obs = dbtypes.pytables_type(str)
    exp = tb.StringCol(16)
    assert_equal(obs, exp)
