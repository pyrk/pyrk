# conductivity_c calculates the thermal conductivity of for a
# range of temperatures, 371 [K] - 1500 [K].
# This comes from Fink and Leibowitz, 1995
# Their paper is called "Thermodynamic and Transport Properties of 
# Sodium Liquid and Vapor," pg. 181.
# 
# T   =   T_c+273.15;
# k_c =   124.67-0.11381*T+5.5226*10^(-5)*T.^2-1.1842*10^(-8)*T.^3;


def k_flibe(t_flibe):
    return 50 # placeholder
