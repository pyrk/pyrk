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
