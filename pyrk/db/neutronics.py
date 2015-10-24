"""
This module creates a table to store information about neutronics behavior in the
simulation.
"""

from __future__ import print_function

import tables as tb


class NeutronicsParamRow(tb.IsDescription):
    """<++>

    :param <++>: <++>
    :type <++>: <++>
    """
    t_idx = tb.Int32Col()
    t = tb.Float64Col()
    power_tot = tb.Float64Col()
    rho_tot = tb.Float64Col()
    rho_ext = tb.Float64Col()


class NeutronicsTimeseriesRow(tb.IsDescription):
    """<++>

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """
    t_idx = tb.Int32Col()
    t = tb.Float64Col()
    component = tb.StringCol(16)  # 16 character string
    power = tb.Float64Col()
    rho = tb.Float64Col()


class ZetasTimestepRow(tb.IsDescription):
    """<++>

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """
    t_idx = tb.Int32Col()
    t = tb.Float64Col()
    zeta_idx = tb.Float64Col()
    zeta = tb.Float64Col()


class OmegasTimestepRow(tb.IsDescription):
    """<++>

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """
    t_idx = tb.Int32Col()
    t = tb.Float64Col()
    omega_idx = tb.Float64Col()
    omega = tb.Float64Col()


def make_neutronics_group(db):
    """Create a group to hold the neutronics stuff

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """
    neutronics_group = db.add_group(groupname='neutronics',
                                    grouptitle='Neutronics',
                                    path_to_group='/')
    return neutronics_group


def make_tables(db):
    """Adds tables to hold information about neutronics in the database

    :param db: The pyrk backend database object
    :type db: Database object.
    """
    n_table = db.add_table(groupname='neutronics',
                           tablename='neutronics',
                           description=NeutronicsTimestepRow,
                           tabletitle="Neutronics Total")

    n_components_table = db.add_table(groupname='neutronics',
                                      tablename='neutronics_components',
                                      description=NeutronicsComponentTimestepRow,
                                      tabletitle="Neutronics Components")

    zetas_table = db.add_table(groupname='neutronics',
                               tablename='zetas',
                               description=ZetasTimestepRow,
                               tabletitle="Neutron Precursors")

    omegas_table = db.add_table(groupname='neutronics',
                                tablename='omegas',
                                description=OmegasTimestepRow,
                                tabletitle="Decay Heat Omegas")

    return n_table, n_components_table, zetas_table, omegas_table


def add_n_entry(table):
    """

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """


def add_n_components_entry(table):
    """

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """


def add_zetas_entry(table):
    """

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """


def add_omegas_entry(table):
    """

    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    :param <++>: <++>
    :type <++>: <++>
    """
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
