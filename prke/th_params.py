
class THParams(object):
    """This holds the parameters for the PB-FHR. For other reactors, implement 
    your own damn class."""

    def __init__(self):
        self._components = ["fuel", "cool", "mod", "refl"]
        # below from greenspan/cisneros
        self._init_temps = {
                "fuel": [730.0],
                "cool": [650.0],
                "mod": [700.0],
                "refl": [650.0]
                }
    # conductivity_c calculates the thermal conductivity of for a
    # range of temperatures, 371 [K] - 1500 [K].
    # This comes from Fink and Leibowitz, 1995
    # Their paper is called "Thermodynamic and Transport Properties of 
    # Sodium Liquid and Vapor," pg. 181.
    # 
    # T   =   t_cool+273.15
    # k_c =   124.67-0.11381*T+5.5226*10^(-5)*T.^2-1.1842*10^(-8)*T.^3
        
    def k(component, temp):
        if component == "fuel":
            return k_fuel(temp)
        elif component == "cool":
            return k_cool(temp)
        elif component == "mod":
            return k_graphite(temp)
        elif component == "refl":
            return k_graphite(temp)
        else :
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")


    def k_cool(self, _cool):
        # http://www.psfc.mit.edu/library1/catalog/reports/1980/80rr
        # /80rr012/80rr012_full.pdf
        # would prefer temperature dependent thermal conductivity?
        # [W/m-K]
        return 1.0 

    # k_fuel calculates the thermal conductivity of the fuel.   Metal fuel data can 
    # be found in a Pu-40Zr metal fuel in Metallic fuels for advanced reactors  
    # W.J.Carmac & D.L.Porter:  Average Value over Predicted Range of Temepratures
    # [W/m-K]
    # in the pbmr, they use zehner-schlunder to approximate k_eff for the pebble 
    # bed:
    # http://www.sciencedirect.com/science/article/pii/S0029549306000185
    # here is a paper on that approximation:
    # http://ac.els-cdn.com/0017931094903921/1-s2.0-0017931094903921-main.pdf
    # ?_tid=e7d08bac-b380-11e3-90e0-00000aacb35f&acdnat
    # =1395685377_d73165eba81bc145ccebc98c195abf36
    def k_fuel(self, t_fuel):
        k = 20 # this is what's assumed for the pbmr pebble bed... 
        return k

    # density_coolant(t_cool) describes the density of cool as a function of 
    # temperature
    # This comes from :
    # http://aries.ucsd.edu/raffray/publications/FST/TOFE_15_Zaghloul.pdf
    # it is valid between the melting point and the critical point

    def k_graphite(self, t_graphite):
        # TODO : get a number for this
        return 0

    def rho_cool(self, t_cool):
        """The density of the cool coolant"""
        # melting point [K]
        t_m = 732.2
        # critical point [K]
        t_c = 4498.8
        # rho correlation [kg/m^3]
        rho = 2415.6 - 0.49072*t_cool
        return rho

    # density_f describes the density of the fuel a function of temperature.
    # From From a Pu-40Zr metal fuel in Metallic fuels for advanced reactors
    # W.J.Carmac & D.L.Porter.
    # Average Value over Predicted Range of Temepratures
    # [kg/m^3]


    # MUST UPDATE: THE BELOW IS STILL FOR METAL FUEL
    def rho_fuel(self, t_fuel):
        """density of the fuel in [kg/m^3]"""
        T_o     =   298.15
        rho_o   =   14100
        alpha   =   17.0*10^-6
        rho     =   rho_o/(1 + alpha*(T-T_o))
        return rho


    # h_conv calculates the heat tranfer coefficient between the coolant the fuel.
    # This taken from Todreas, N.E., Kazimi, M.S., 1990. Nuclear Systems: I. 
    # Thermal Hydraulic Fundamentals. Taylor & Francis.
    # Westinghouse Correlation for metal coolant flowing parallel to rod
    # bundles.
    # run variables
    # Re  =   density_c(t_cool)*u*D_h./viscosity_c(t_cool)
    # Pr  =   viscosity_c(t_cool).*cp_c(t_cool)./conductivity_c(t_cool)
    # Pe  =   Re*Pr
    # Nu  =   4.0+0.33*P2D^(3.8)*(Pe/100).^(0.86)+0.16*(P2D)^5
    # h   =   Nu.*conductivity_c(t_cool)/D_h

    def h_conv(self, t_cool):
        return 27000


    # cp_c is the heat capacity at constant pressure as a function of Temperature
    # This came from Fink and Leibowitz 
    # It is the polynomial approximation in equation 35 in the paper called 
    # Thermodynamic and transport properties of Sodium Liquid and Vapor
    # [J/kg-K]
    # T   =   t_cool+273.15
    # c_p = 1.6582 - (8.4790*10^(-4))*T + (4.4541*10^(-7))*T.^2 - 2992.6*T.^(-2)
    # c_p =   1277
    def spec_heat_c(self, t_cool):
        R   =   therm_resist(1,1)
        con =   (A_fuel*H_core)/(A_flow*2*u*R)*(T_f_o-t_cool_o)/(t_cool_o-T_in)
        c_p =   con/density_c(t_cool)
        return c_p

    # cp_f is the heat capacity at constant pressure as a function of temperature
    # From From a Pu-40Zr metal fuel in Metallic fuels for advanced reactors
    # W.J.Carmac & D.L.Porter.
    # Average Value over Predicted Range of Temepratures
    # [J/kg-K]
    def spec_heat_f(self, t_fuel):
        c_p =   161
        return c_p

    # therm_resist calcualtes the termal resistance between the coolant and the
    # fuel.
    def therm_resist(self, t_fuel, t_cool):
        r_th = (T_f_o-T_c_o)/(omega);
        return r_th
    # con1    =   1/(2*pi*k_clad)*log(R_clad/R_fuel);
    # con2    =   1/(2*pi*R_clad*h_conv(T_c));
    # con3    =   w/(4*pi*conductivity_f(T_f));
    # R_th    =   A_fuel*(con1+con2+con3);
