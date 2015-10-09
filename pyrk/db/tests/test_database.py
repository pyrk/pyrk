from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from db import database as d


def test_default_constructor():
    a = d.Database()
    assert_equal(a.mode, 'a')
    assert_equal(a.title, 'PyRKDatabase')
    import os.path
    assert_true(os.path.isfile(a.filepath))


def test_custom_constructor():
    a = d.Database(filepath='testfile.h5')
    assert_equal(a.filepath, 'testfile.h5')
