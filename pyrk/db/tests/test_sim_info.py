from nose.tools import assert_equal, assert_almost_equal, assert_true, \
    assert_false, assert_raises, assert_is_instance, with_setup

from db import database as d
from db import sim_info_table as c

import unittest


class SimInfoTest(unittest.TestCase):
    def setUp(self):
        "set up test fixtures"
        self.a = d.Database()

    def tearDown(self):
        "tear down test fixtures"
        self.a.delete_db()

    def test_sim_info_group(self):
        grp_str = self.a.h5file.root.metadata.__str__()
        assert_true('Simulation Information' in grp_str)

    def test_add_entry(self):
        rec = {'t0': 0.0,
               'tf': 10.0,
               'dt': 0.1,
               't_feedback': 1.0,
               'iso': 'u235',
               'e': 'thermal',
               'n_pg': 1,
               'n_dg': 1,
               'kappa': 0.0,
               'plotdir': 'images'}
        d.add_row(self.a.h5file.root.metadata.sim_info, rec)
        t0_obs = self.tab.col('t0')
        t0_exp = 0.0
        assert_equal(t0_obs, t0_exp)
        tf_obs = self.tab.col('tf')
        tf_exp = 10.0
        assert_equal(tf_obs, tf_exp)
