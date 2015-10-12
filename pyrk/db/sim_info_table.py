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


def make_th_group(db):
    # Create a group for the table
    th_group = db.add_group(groupname='th',
                            grouptitle='TH',
                            path_to_group='/')
    return th_group


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


def add_entry(table,
              t0=0.0,
              tf=10.0,
              dt=0.1,
              t_feedback=10,
              iso='u235',
              e='thermal',
              n_pg=1,
              n_dg=1,
              kappa=0.0,
              plotdir='images'):
    table.row['t0'] = t0
    table.row['tf'] = tf
    table.row['dt'] = dt
    table.row['t_feedback'] = t_feedback
    table.row['iso'] = iso
    table.row['e'] = e
    table.row['n_pg'] = n_pg
    table.row['n_dg'] = n_dg
    table.row['kappa'] = kappa
    table.row['plotdir'] = plotdir
    table.row.append()


def add_entry_from_sim_info(table, si):
    add_entry(table,
              t0=si.timer.t0,
              tf=si.timer.tf,
              dt=si.timer.dt,
              t_feedback=si.t_feedback,
              iso=si.iso,
              e=si.e,
              n_pg=si.n_pg,
              n_dg=si.n_dg,
              kappa=si.kappa,
              plotdir=si.plotdir)
