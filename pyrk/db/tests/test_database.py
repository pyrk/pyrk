from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from db import database as d

import unittest


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        "set up test fixtures"
        self.a = d.Database()

    def tearDown(self):
        "tear down test fixtures"
        self.a.delete_db()

    def test_default_constructor(self):
        assert_equal(self.a.mode, 'a')
        assert_equal(self.a.title, 'PyRKDatabase')
        import os.path
        assert_true(os.path.isfile(self.a.filepath))

    def test_add_group(self):
        self.a.add_group(groupname="test_group",
                         grouptitle="Test Group",
                         path_to_group="/")
        assert_true('Test Group' in self.a.h5file.root.test_group.__str__())

    def test_custom_constructor(self):
        a = d.Database(filepath='testfile.h5')
        assert_equal(a.filepath, 'testfile.h5')
        # cleanup
        a.delete_db()
