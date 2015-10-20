from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from db import database as d
from db import components as c

import unittest


class ComponentsTest(unittest.TestCase):
    def setUp(self):
        "set up test fixtures"
        self.a = d.Database()

    def tearDown(self):
        "tear down test fixtures"
        self.a.delete_db()

    def test_th_group(self):
        c.make_th_group(self.a)
        grp_str = self.a.h5file.root.th.__str__()
        assert_true('TH' in grp_str)
