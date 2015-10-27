# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb
import descriptions as desc


import contextlib
import sys


@contextlib.contextmanager
def nostderr():
    savestderr = sys.stderr

    class Devnull(object):
        def write(self, _): pass

        def flush(self): pass

    sys.stderr = Devnull()
    try:
        yield
    finally:
        sys.stderr = savestderr


@contextlib.contextmanager
def open_h5(db):
    db.open_db()
    try:
        yield db
    finally:
        db.close_db()


class Database(object):
    """The Database class handles operations on the pyrk simulation backend and
    provides utilities for interacting with it.
    """

    def __init__(self, filepath='pyrk.h5',
                 mode='a',
                 title='PyRKDatabase'
                 ):
        """Creates an hdf5 database for simulation information

        :param filepath: the location of the h5 file. e.g. 'pyrk.h5'
        :type filepath: str
        :param mode: mode for file opening
        :type mode: str (a, w, and r are supported)
        :param title: The title of the database
        :type title: str
        """
        self.mode = mode
        self.title = title
        self.h5file = tb.open_file(filepath,
                                   mode=self.mode,
                                   title=self.title)
        self.filepath = filepath
        self.groups = self.set_up_groups()
        self.tables = self.set_up_tables()
        self.make_groups()
        self.make_tables()
        self.recorders = {}

    def add_group(self, groupname, grouptitle, path_to_group='/'):
        """Creates a new group in the file

        :param groupname: name of the group to add
        :type groupname: str
        :param grouptitle: metadata to store in plain english, a title
        :type grouptitle: str
        :param path_to_group: the database path, starts with '/'
        :type path_to_group: str
        """
        self.open_db()
        group = self.group_exists(path_to_group, groupname)
        if group is False:
            group = self.h5file.create_group(path_to_group, groupname,
                                             grouptitle)
        return group

    def add_table(self, groupname, tablename, description, tabletitle):
        """Creates a new table
        All groupnames must be directly under root"""
        self.open_db()
        table = self.h5file.create_table('/'+groupname,
                                         tablename,
                                         description,
                                         tabletitle)
        return table

    def add_row(self, table, row_dict):
        self.open_db()
        for k, v in row_dict.iteritems():
            table.row[k] = v
        table.row.append()
        table.flush()

    def group_exists(self, path_to_group, groupname):
        self.open_db()
        try:
            group = self.h5file.get_node(path_to_group,
                                         name=groupname)
        except tb.NoSuchNodeError:
            group = False
        return group

    def open_db(self):
        """Returns a handle to the open db"""
        # if it is not open, open it.
        if self.h5file.isopen is False:
            self.h5file = tb.open_file(self.filepath, mode='a')
        return self.h5file

    def close_db(self):
        with nostderr():
            tb.file._open_files.close_all()

    def record_all(self):
        self.open_db()
        for t, r in self.recorders.iteritems():
            self.add_row(t, r())
        self.close_db()

    def delete_db(self):
        """If the database exists, delete it"""
        import os.path
        os.remove(self.filepath)

    def make_groups(self):
        for g in self.groups:
            self.add_group(groupname=g['groupname'],
                           grouptitle=g['grouptitle'],
                           path_to_group=g['path'])

    def make_tables(self):
        for t in self.tables:
            self.add_table(groupname=t['groupname'],
                           tablename=t['tablename'],
                           description=t['description'],
                           tabletitle=t['tabletitle'])

    def set_up_groups(self):
        groups = []
        groups.append({'groupname': 'th',
                       'grouptitle': 'TH',
                       'path': '/'})
        groups.append({'groupname': 'neutronics',
                       'grouptitle': 'Neutronics',
                       'path': '/'})
        groups.append({'groupname': 'metadata',
                       'grouptitle': 'Simulation Metadata',
                       'path': '/'})
        return groups

    def set_up_tables(self):
        tables = []
        tables.append({'groupname': 'th',
                       'tablename': 'th_params',
                       'description': desc.ThMetadataRow,
                       'tabletitle': 'TH Component Parameters'})
        tables.append({'groupname': 'th',
                       'tablename': 'th_timeseries',
                       'description': desc.ThTimeseriesRow,
                       'tabletitle': 'TH Timeseries'})
        tables.append({'groupname': 'metadata',
                       'tablename': 'sim_info',
                       'description': desc.SimInfoRow,
                       'tabletitle': 'Simulation Information'})
        tables.append({'groupname': 'neutronics',
                       'tablename': 'neutronics_timeseries',
                       'description': desc.NeutronicsTimeseriesRow,
                       'tabletitle': 'Neutronics Timeseries'})
        tables.append({'groupname': 'neutronics',
                       'tablename': 'neutronics_params',
                       'description': desc.NeutronicsParamsRow,
                       'tabletitle': 'Neutronics Metadata'})
        tables.append({'groupname': 'neutronics',
                       'tablename': 'zetas',
                       'description': desc.ZetasTimestepRow,
                       'tabletitle': 'Neutron Precursor Concentrations'})
        tables.append({'groupname': 'neutronics',
                       'tablename': 'omegas',
                       'description': desc.OmegasTimestepRow,
                       'tabletitle': 'Decay Heat Fractions'})
        return tables

    def register_recorder(self, groupname, tablename, recorder):
        self.open_db()
        tab = self.get_table(groupname, tablename)
        self.recorders[tab] = recorder

    def get_table(self, grp, tbl):
        self.open_db()
        return self.h5file.root._f_get_child(grp)._f_get_child(tbl)
