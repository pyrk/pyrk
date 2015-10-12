"""
This module creates a table to store information about simulation itself.
"""

from __future__ import print_function

import tables as tb


class SimInfoParamsRow(tb.IsDescription):
    """This describes a SimInfoParams record structure"""
    sim = tb.Int64Col()            # 64 bit float
    t0 = tb.Float64Col()            # 64 bit float
    tf = tb.Float64Col()            # 64 bit float
    dt = tb.Float64Col()            # 64 bit float
    t_feedback = tb.Float64Col()    # 64 bit float
    iso = tb.StringCol(16)
    e = tb.StringCol(16)
    n_pg = tb.Int32Col()
    n_dg = tb.Int32Col()
    kappa = tb.Float64Col()
    plotdir = tb.StringCol(16)


def make_sim_info_group(db):
    # Create a group for the tables related to simulation information
    sim_info_group = db.add_group(groupname='sim_info',
                                  grouptitle='Simulation Info',
                                  path_to_group='/')
    return sim_info_group


def make_sim_info_params_table(db, sim_info):
    """Adds a sim_info_params table to hold information about each simulation
    in the database

    :param db: The pyrk backend database object
    :type db: Database object.
    :param sim_info: List of the sim_info to record
    :type sim_info: list(SimInfo)
    """
    sim_info_params_table = db.add_table(groupname='th',
                                         tablename='th_params',
                                         description=SimInfoParamsRow,
                                         tabletitle="Simulation Parameters")
    return sim_info_params_table


def add_entry(table, rec):
    for k, v in rec:
        table.row[k] = v
    table.row.append()
    table.flush()


def add_entry_from_sim_info(table, si):
    add_entry(table, si.record())
