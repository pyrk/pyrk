function rho = reactivity(t,T_f,T_c)
run variables
N   =   length(t);
rho =   zeros(4,N);
for i=1:N
    rho(1,i)    =   reactivity_external(t(i));
    rho(2,i)    =   alpha_d*(T_f(i).^d-T_f_o.^d);
    rho(3,i)    =   alpha_c*(T_c(i)-T_c_o);
end
rho(4,:)    =   rho(1,:)+rho(2,:)+rho(3,:);
end
