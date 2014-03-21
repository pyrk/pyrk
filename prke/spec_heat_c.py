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



