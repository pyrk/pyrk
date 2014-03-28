# conductivity_c calculates the thermal conductivity of for a
# range of temperatures, 371 [K] - 1500 [K].
# This comes from Fink and Leibowitz, 1995
# Their paper is called "Thermodynamic and Transport Properties of 
# Sodium Liquid and Vapor," pg. 181.
# 
# T   =   T_c+273.15;
# k_c =   124.67-0.11381*T+5.5226*10^(-5)*T.^2-1.1842*10^(-8)*T.^3;


def k_flibe(t_flibe):
    # from http://www.psfc.mit.edu/library1/catalog/reports/1980/80rr/80rr012/80rr012_full.pdf
    # would prefer temperature dependent thermal conductivity?
    # [W/m-K]
    return 1.0 
# k_fuel calculates the thermal conductivity of the fuel.   Metal fuel data can 
# be found in a Pu-40Zr metal fuel in Metallic fuels for advanced reactors  
# W.J.Carmac & D.L.Porter:  Average Value over Predicted Range of Temepratures
# [W/m-K]
# I guess in the pbmr, they use Zehner–Schlünder to approximate the effective k 
# for the pebble bed :
# http://www.sciencedirect.com/science/article/pii/S0029549306000185
# here's a paper on that approximation:
# http://ac.els-cdn.com/0017931094903921/1-s2.0-0017931094903921-main.pdf?_tid=e7d08bac-b380-11e3-90e0-00000aacb35f&acdnat=1395685377_d73165eba81bc145ccebc98c195abf36
def k_fuel(t_fuel):
    k = 20 # this is what's assumed for the pbmr pebble bed... 
    return k

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


function h  =   h_conv(T_c)
# h_conv calculates the heat tranfer coefficient between the coolant the fuel.
# This taken from Todreas, N.E., Kazimi, M.S., 1990. Nuclear Systems: I. 
# Thermal Hydraulic Fundamentals. Taylor & Francis.
# Westinghouse Correlation for metal coolant flowing parallel to rod
# bundles.
# run variables
# Re  =   density_c(T_c)*u*D_h./viscosity_c(T_c);
# Pr  =   viscosity_c(T_c).*cp_c(T_c)./conductivity_c(T_c);
# Pe  =   Re*Pr;
# Nu  =   4.0+0.33*P2D^(3.8)*(Pe/100).^(0.86)+0.16*(P2D)^5;
# h   =   Nu.*conductivity_c(T_c)/D_h;

def h_conv(t_flibe):
    return 27000
function c_p = specheat_c(T_c)
% cp_c is the heat capacity at constant pressure as a function of Temperature
% This came from Fink and Leibowitz 
% It is the polynomial approximation in equation 35 in the paper called 
% Thermodynamic and transport properties of Sodium Liquid and Vapor
% [J/kg-K]
% T   =   T_c+273.15;
% c_p = 1.6582 - (8.4790*10^(-4))*T + (4.4541*10^(-7))*T.^2 - 2992.6*T.^(-2);
% c_p =   1277;
run variables
R   =   therm_resist(1,1);
con =   (A_fuel*H_core)/(A_flow*2*u*R)*(T_f_o-T_c_o)/(T_c_o-T_in);
c_p =   con/density_c(T_c);
end



function c_p = specheat_f(T_f)
% cp_f is the heat capacity at constant pressure as a function of temperature
% From From a Pu-40Zr metal fuel in Metallic fuels for advanced reactors
% W.J.Carmac & D.L.Porter.
% Average Value over Predicted Range of Temepratures
% [J/kg-K]
c_p =   161;
end


