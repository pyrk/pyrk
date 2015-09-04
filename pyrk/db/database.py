# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


class Database(object):
    """The Database class handles operations on the pyrk simulation backend and
    provides utilities for interacting with it.
    """

    def __init__(self, filepath):
        """Creates an hdf5 database at filepath"""
        self.h5file = tb.open_file(filepath,
                                   mode="w",
                                   title="PyRK Database")

    def add_group(self, groupname, grouptitle):
        """Creates a new group in the file"""
        group = self.h5file.create_group("/",
                                         groupname,
                                         grouptitle)

    def add_table(self, groupname, tablename, description, tabletitle):
        """Creates a new table"""
        table = self.h5file.create_table(groupname,
                                         tablename,
                                         description,
                                         tabletitle)

    def add_timestep(self, timestep):
        """Adds data from a timestep"""

    def open_db(self):
        """Returns a handle to the open db"""
        return self.h5file
