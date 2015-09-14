"""
This module creates a table to store information about components in the
simulation.
"""

from __future__ import print_function

import tables as tb
from dbtypes import pytables_type


class ThComponentRow(tb.IsDescription):
    """This describes a Component record structure"""

    name = tb.StringCol(16)  # 16 character string
    vol = tb.Float64Col()            # 32 bit float
    k = tb.Int32Col()     # 32 bit integer column
    cp = tb.Float64Col()
    T0 = tb.Float64Col()
    alpha_temp = tb.Float64Col()
    heatgen = tb.Float64Col()
    power_tot = pytables_type(float)


def make_components_table(db, components):
    """Adds a components table to hold information about each component in the
    database

    :param db: The pyrk backend database object
    :type db: Database object.
    :param components: List of the components to record
    :type components: list(Component)
    """

    # Open the hdf5 file
    db_file = tb.openFile(db, 'a')

    # Create a group for the table
    th_group = db_file.createGroup("/", "th", "TH")

    # Make the new table
    th_params_table = db_file.create_table(th_group, 'th_params',
                                           ThComponentRow,
                                           "TH Component Params")

    # Ensure that data was written to table
    th_params_table.flush()

    # Close the hdf5 file
    db_file.close()
