# density_f describes the density of the fuel a function of temperature.
# From From a Pu-40Zr metal fuel in Metallic fuels for advanced reactors
# W.J.Carmac & D.L.Porter.
# Average Value over Predicted Range of Temepratures
# [kg/m^3]


# MUST UPDATE: THE BELOW IS STILL FOR METAL FUEL
def rho_fuel(t_fuel):
    """density of the fuel in [kg/m^3]""""
    T_o     =   298.15;
    rho_o   =   14100;
    alpha   =   17.0*10^-6;
    rho     =   rho_o/(1 + alpha*(T-T_o));
    return rho

 


