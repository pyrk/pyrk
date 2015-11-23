# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


class NeutronicsParamsRow(tb.IsDescription):
    """<++>

    :param <++>: <++>
    :type <++>: <++>
    """
    t_idx = tb.Int32Col()
    component = tb.StringCol(16)
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
    component = tb.StringCol(16)
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
    omega_idx = tb.Float64Col()
    omega = tb.Float64Col()


class ThTimeseriesRow(tb.IsDescription):
    t_idx = tb.Int64Col()
    component = tb.StringCol(16)
    temp = tb.Float64Col()
    density = tb.Float64Col()
    k = tb.Float64Col()
    cp = tb.Float64Col()
    alpha_temp = tb.Float64Col()
    heatgen = tb.BoolCol()
    power_tot = tb.Float64Col()


class ThMetadataRow(tb.IsDescription):
    """This describes a THComponentParams record structure"""
    component = tb.StringCol(16)
    vol = tb.Float64Col()
    matname = tb.StringCol(16)
    k = tb.Float64Col()
    cp = tb.Float64Col()
    T0 = tb.Float64Col()
    alpha_temp = tb.Float64Col()
    heatgen = tb.BoolCol()
    power_tot = tb.Float64Col()


class SimInfoRow(tb.IsDescription):
    """This describes a SimInfoParams record structure"""
    sim = tb.Int64Col()
    t0 = tb.Float64Col()
    tf = tb.Float64Col()
    dt = tb.Float64Col()
    t_feedback = tb.Float64Col()
    iso = tb.StringCol(16)
    e = tb.StringCol(16)
    n_pg = tb.Int32Col()
    n_dg = tb.Int32Col()
    kappa = tb.Float64Col()
    plotdir = tb.StringCol(16)


class SimInputRow(tb.IsDescription):
    """This describes a simulation record structure"""
    simhash = tb.StringCol(16)
    timestamp = tb.Int64Col()
    humantime = tb.StringCol(16)
    revision = tb.StringCol(16)
    # pytables can't handle VL strings
    # a long input file might be 10000 bytes
    # for now, anything longer will be cut off...
    inputblob = tb.StringCol(10000)
