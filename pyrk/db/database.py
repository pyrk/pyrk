# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


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
        self.close_db()

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
            group = self.h5file.create_group(path_to_group,
                                             groupname,
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
        for k, v in row_dict.iteritems():
            table.row[k] = v
        table.row.append()

    def group_exists(self, path_to_group, groupname):
        try:
            group = self.h5file.get_node(path_to_group,
                                         name=groupname)
        except tb.NoSuchNodeError:
            group = False
        return group

    def open_db(self):
        """Returns a handle to the open db"""
        #  make sure that it's open.
        self.h5file = tb.open_file(self.filepath, mode='a')

    def close_db(self):
        self.h5file = self.h5file.close()

    def delete_db(self):
        """If the database exists, delete it"""
        import os.path
        os.remove(self.filepath)
