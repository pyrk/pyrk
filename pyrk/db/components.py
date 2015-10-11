"""
This module creates a table to store information about components in the
simulation.
"""

from __future__ import print_function

import tables as tb


class ThComponentRow(tb.IsDescription):
    """This describes a Component record structure"""

    name = tb.StringCol(16)  # 16 character string
    vol = tb.Float64Col()            # 32 bit float
    matname = tb.StringCol(16)
    k = tb.Float64Col()     # 32 bit integer column
    cp = tb.Float64Col()
    T0 = tb.Float64Col()
    alpha_temp = tb.Float64Col()
    heatgen = tb.Float64Col()
    power_tot = tb.Float64Col()


def make_th_group(db):
    # Create a group for the table
    th_group = db.add_group(groupname='th',
                            grouptitle='TH',
                            path_to_group='/')
    return th_group


def make_th_params_table(db, components):
    """Adds a th_params table to hold information about each th component in the
    database

    :param db: The pyrk backend database object
    :type db: Database object.
    :param components: List of the components to record
    :type components: list(Component)
    """
    th_params_table = db.add_table(groupname='th',
                                   tablename='th_params',
                                   description=ThComponentRow,
                                   tabletitle="TH Component Parameters")
    return th_params_table

def add_entry(table):
    table.row['name'] = 'fuel'
    table.row['vol'] = 10.0
    table.row['matname'] = 'triso'
    table.row['k'] = 10
    table.row['cp'] = 92.0
    table.row['T0'] = 92.0
    table.row['alpha_temp'] = 92.0
    table.row['heatgen'] = 92.0
    table.row['powertot'] = 92.0
    table.row.append()
