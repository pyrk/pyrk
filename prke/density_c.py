# density_coolant(T_c) describes the density of flibe as a function of 
# temperature
# This comes from :
# http://aries.ucsd.edu/raffray/publications/FST/TOFE_15_Zaghloul.pdf
# it is valid between the melting point and the critical point

def rho_flibe(t_flibe):
    """The density of the flibe coolant"""
    # melting point [K]
    t_m = 732.2
    # critical point [K]
    t_c = 4498.8
    # rho correlation [kg/m^3]
    rho = 2415.6 - 0.49072*t_flibe
    return rho



