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


class SimulationRow(tb.IsDescription):
    """This describes a simulation record structure"""
    simhash = tb.Int64Col()            # 64 bit float
    # pytables can't handle VL strings
    # a long input file might be 10000 bytes
    # for now, anything longer will be cut off...
    inputblob = tb.StringCol(10000)
    revision = tb.StringCol(16)


def make_sim_info_group(db):
    # Create a group for the tables related to simulation information
    sim_info_group = db.add_group(groupname='sim_info',
                                  grouptitle='Simulation Info',
                                  path_to_group='/')
    return sim_info_group


def make_sim_info_params_table(db):
    """Adds a sim_info_params table to hold information about each simulation
    in the database

    :param db: The pyrk backend database object
    :type db: Database object.
    """
    sim_info_params_table = db.add_table(groupname='sim_info',
                                         tablename='sim_info_params',
                                         description=SimInfoParamsRow,
                                         tabletitle="Simulation Parameters")
    return sim_info_params_table


def add_entry(table, rec):
    for k, v in rec.iteritems():
        table.row[k] = v
    table.row.append()
    table.flush()


def add_entry_from_sim_info(table, si):
    add_entry(table, si.record())


def get_sim_hash():
    return 'nonsense, fixme'


def get_input_blob():
    return 'nonsense, fixme'


def add_simulation(table):
    rec = {}
    rec['simhash'] = get_sim_hash()
    rec['inputblob'] = get_input_blob()
    import pyrk
    rec['revision'] = pyrk.__version__
    add_entry(table, rec)
