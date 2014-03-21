function mu =   viscosity_c(T_c)
% viscosity calculates the viscosity of the 
% This comes from Fink and Leibowitz, 1995
% Their paper is called "Thermodynamic and Transport Properties of 
% Sodium Liquid and Vapor," pg. 207.
% T   =   T_c+273.15;
% mu  =   exp(-6.4406-0.3958*log(T)+556.835/T);
mu  =   0.00018;
end
