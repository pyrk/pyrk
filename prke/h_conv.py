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
