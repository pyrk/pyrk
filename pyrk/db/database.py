# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


class Database(object):
    """The Database class handles operations on the pyrk simulation backend and
    provides utilities for interacting with it.
    """

    def __init__(self, filepath):
        """Creates an hdf5 database at filepath"""
        h5file = open_file(filepath, mode = "w", title = "PyRK Database")


    def add_table(self, tablename):
        """Creates a new table"""

    def add_timestep(self, timestep):
        """Adds data from a timestep"""

    def open_db(self):
        """Returns a handle to the open db"""
