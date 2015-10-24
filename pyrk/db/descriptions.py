# Licensed under a 3-clause BSD style license - see LICENSE
import tables as tb


class NeutronicsParamsRow(tb.IsDescription):
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


class ThTimeseriesRow(tb.IsDescription):
    t_idx = tb.Int32Col()
    t = tb.Float64Col()
    component = tb.StringCol(16)  # 16 character string
    temp = tb.Float64Col()            # 32 bit float
    matname = tb.StringCol(16)
    k = tb.Float64Col()     # 32 bit integer column
    cp = tb.Float64Col()
    T0 = tb.Float64Col()
    alpha_temp = tb.Float64Col()
    heatgen = tb.Float64Col()
    power_tot = tb.Float64Col()


class ThMetadataRow(tb.IsDescription):
    """This describes a THComponentParams record structure"""
    name = tb.StringCol(16)  # 16 character string
    vol = tb.Float64Col()            # 32 bit float
    matname = tb.StringCol(16)
    k = tb.Float64Col()     # 32 bit integer column
    cp = tb.Float64Col()
    T0 = tb.Float64Col()
    alpha_temp = tb.Float64Col()
    heatgen = tb.Float64Col()
    power_tot = tb.Float64Col()


class SimInfoRow(tb.IsDescription):
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
    timestep = tb.Int64Col()            # 64 bit float
    # pytables can't handle VL strings
    # a long input file might be 10000 bytes
    # for now, anything longer will be cut off...
    inputblob = tb.StringCol(10000)
    revision = tb.StringCol(16)
