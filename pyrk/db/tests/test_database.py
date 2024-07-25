from pyrk.db import database as d

import pytest

def dictfunc():
    return {'t0': 2}

class TestDatabase:

    @pytest.fixture(autouse=True)
    def resource(self):
        "set up test fixtures"
        self.a = d.Database(mode='w')
        self.custom = d.Database(filepath='testfile.h5', mode='w')
        yield "resource"
        "tear down test fixtures"
        self.a.close_db()
        self.a.delete_db()
        self.custom.close_db()
        self.custom.delete_db()

    def test_default_constructor(self):
        assert self.a.mode == 'w'
        assert self.a.title == 'PyRKDatabase'
        import os.path
        assert os.path.isfile(self.a.filepath)

    def test_add_group(self):
        self.a.add_group(groupname="test_group",
                         grouptitle="Test Group",
                         path_to_group="/")
        assert 'Test Group' in self.a.h5file.root.test_group.__str__()

    def test_group_exists(self):
        assert self.a.group_exists('/', 'metadata')

    def test_open_and_close_db(self):
        self.a.open_db()
        assert self.a.h5file.isopen
        self.a.close_db()
        assert not self.a.h5file.isopen
        self.a.open_db()
        assert self.a.h5file.isopen

    def test_open_and_close_custom_db(self):
        assert self.custom.filepath == 'testfile.h5'
        self.custom.open_db()
        assert self.custom.h5file.isopen
        self.custom.close_db()
        assert not self.custom.h5file.isopen
        self.custom.open_db()
        assert self.custom.h5file.isopen

    def test_register_recorder(self):
        self.a.register_recorder('metadata', 'sim_info', dictfunc,
                                 timeseries=True)
        assert any(dictfunc in r for r in self.a.recorders)

    def test_custom_constructor(self):
        assert self.custom.filepath == 'testfile.h5'

    def test_sim_info_group(self):
        grp_str = self.a.h5file.root.metadata.__str__()
        assert 'Simulation Metadata' in grp_str

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
        tab = self.a.get_table('metadata', 'sim_info')
        self.a.add_row(tab, rec)
        t0_obs = tab.col('t0')[0]
        t0_exp = rec['t0']
        assert t0_obs == t0_exp
        tf_obs = tab.col('tf')[0]
        tf_exp = rec['tf']
        assert tf_obs == tf_exp

    def test_get_table(self):
        self.a.open_db()
        exp_cols = self.a.h5file.root.metadata.sim_info.coldescrs
        obs_cols = self.a.get_table('metadata', 'sim_info').coldescrs
        assert exp_cols == obs_cols

    def test_set_up_tables(self):
        tables = self.a.set_up_tables()
        for t in tables:
            assert t['groupname'] in ['th',
                                           'metadata',
                                           'neutronics']
            assert t['tablename'] in ['th_params', 'th_timeseries',
                                           'sim_info',
                                           'sim_timeseries',
                                           'neutronics_timeseries',
                                           'neutronics_params',
                                           'zetas',
                                           'omegas'
                                           ]

    def test_set_up_groups(self):
        groups = self.a.set_up_groups()
        for g in groups:
            assert g['groupname'] in ['th',
                                           'metadata',
                                           'neutronics']
