function R_th   =   therm_resist(T_f,T_c)
% therm_resist calcualtes the termal resistance between the coolant and the
% fuel.
run variables
% con1    =   1/(2*pi*k_clad)*log(R_clad/R_fuel);
% con2    =   1/(2*pi*R_clad*h_conv(T_c));
% con3    =   w/(4*pi*conductivity_f(T_f));
% R_th    =   A_fuel*(con1+con2+con3);
R_th        =   (T_f_o-T_c_o)/(omega);
end
