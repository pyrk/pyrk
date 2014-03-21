function rho = reactivity_total(t,T_f,T_c)
run variables
rho_1   =   reactivity_external(t);
rho_2   =   alpha_d*(T_f.^d-T_f_o.^d);
rho_3   =   alpha_c*(T_c-T_c_o);
rho     =   rho_1+rho_2+rho_3;
% rho =   0;
end
