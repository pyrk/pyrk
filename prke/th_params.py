import math

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
        # the data below comes form design doc rev c
        self._power_tot=236.0
        self._vol_tot_active = 4.16 # m^3
        self._vol_tot_defuel = 1.03 #m^3
        self._vol_tot_refl = 4.8 #m^3
        self._pebble_porosity = 0.4 
        self._vol_flow_rate = 976.0 # kg/s
        self._vel_cool = 0.54 # m^3/s 
        self._tinlet = 600.0
        self._fuel_matrix_r = 0.005 # [m] ... matrix(4mm) + coating(1mm)
        self._mod_r = 0.025
        self._pebble_r = self._fuel_matrix_r + self._mod_r
        self._kappa = 0.06 # This is an estimate

    def vol(self, component):
        f = self._fuel_matrix_r
        m = self._mod_r
        tot_fuel_pebble_vol = (1 - self._pebble_porosity)*\
                (self._vol_tot_active + self._vol_tot_defuel)
        single_pebble_vol =  (4./3.)*math.pi*(pow(f+m,3))
        if component == "fuel":
            fuel_vol_in_single_pebble = (4./3.)*math.pi*(pow(f+m,3) - pow(m,3))
            fuel_vol = tot_fuel_pebble_vol*fuel_vol_in_single_pebble/single_pebble_vol
            return fuel_vol
        elif component == "cool":
            tot_vol = self._vol_tot_active + self._vol_tot_defuel + \
                    self._vol_tot_refl
            return tot_vol*self._pebble_porosity
        elif component == "mod":
            mod_vol_in_single_pebble = (4./3.)*math.pi*pow(m,3)
            mod_vol = tot_fuel_pebble_vol*mod_vol_in_single_pebble/single_pebble_vol
            return mod_vol
        elif component == "refl":
            return (1 - self._pebble_porosity)*self._vol_tot_refl
        else :
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")

    # Conductivity
    def k(component, temp):
        """Thermal conductivitiy in W/m-K"""
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
        """Thermal conductivitiy in W/m-K for flibe"""
        # http://www.psfc.mit.edu/library1/catalog/reports/1980/80rr
        # /80rr012/80rr012_full.pdf
        # would prefer temperature dependent thermal conductivity?
        # [W/m-K]
        return 1.0 

    def k_fuel(self, t_fuel):
        """Thermal conductivitiy in W/m-K for the triso fuel layer"""
        # [W/m-K]
        # in the pbmr, they use zehner-schlunder to approximate k_eff for the pebble 
        # bed:
        # http://www.sciencedirect.com/science/article/pii/S0029549306000185
        # here is a paper on that approximation:
        # http://ac.els-cdn.com/0017931094903921/1-s2.0-0017931094903921-main.pdf
        # ?_tid=e7d08bac-b380-11e3-90e0-00000aacb35f&acdnat
        # =1395685377_d73165eba81bc145ccebc98c195abf36
        k = 20 # this is what's assumed for the pbmr pebble bed... 
        return k


    def k_graphite(self, t_graphite):
        """Thermal conductivitiy in W/m-K for the graphite moderator and the \
        reflector"""
        # TODO : get a number for this
        return 0

    def rho(self, component, temp):
        """Density, as a function of temperature [kg/m^3]"""
        # SHOULD THIS BE IN GRAMS?
        if component == "fuel":
            return self.rho_fuel(temp)
        elif component == "cool":
            return self.rho_cool(temp)
        elif component == "mod":
            return self.rho_mod(temp)
        elif component == "refl":
            return self.rho_refl(temp)
        else : 
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")

    def rho_cool(self, t_cool):
        """Density, as a function of temperature, of the flibe coolant"""
        # density_coolant(t_cool) describes the density of cool as a function of 
        # temperature
        # This comes from :
        # http://aries.ucsd.edu/raffray/publications/FST/TOFE_15_Zaghloul.pdf
        # it is valid between the melting point and the critical point
        # melting point [K]
        t_m = 732.2
        # critical point [K]
        t_c = 4498.8
        # rho correlation [kg/m^3]
        rho = 2415.6 - 0.49072*t_cool
        return rho

    def rho_fuel(self, t_fuel):
        # density_f describes the density of the fuel a function of temperature.
        # From From a Pu-40Zr metal fuel in Metallic fuels for advanced reactors
        # W.J.Carmac & D.L.Porter.
        # Average Value over Predicted Range of Temepratures
        # [kg/m^3]
        rho = 0 
        return rho

    def rho_graphite(self, t_graphite):
        rho = 0
        return rho

    # MUST UPDATE: THE BELOW IS STILL FOR METAL FUEL
    def rho_fuel(self, t_fuel):
        """density of the fuel in [kg/m^3]"""
        T_o     =   298.15
        rho_o   =   14100
        alpha   =   17.0*pow(10,-6)
        rho     =   rho_o/(1 + alpha*(t_fuel - T_o))
        return rho

    def cp(self, component):
        if component == "fuel":
            return self.cp_fuel()
        elif component == "cool":
            return self.cp_cool()
        elif component == "mod":
            return self.cp_mod()
        elif component == "refl":
            return self.cp_refl()
        else : 
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")

    def cp_fuel(self):
        # cp_f is the heat capacity at constant pressure as a function of temperature
        # From From a Pu-40Zr metal fuel in Metallic fuels for advanced reactors
        # W.J.Carmac & D.L.Porter.
        # Average Value over Predicted Range of Temepratures
        # [J/kg-K]
        # TODO placeholder
        c_p =   161
        return c_p


    def cp_cool(self):
        # cp_c is the heat capacity at constant pressure as a function of Temperature
        # This came from Fink and Leibowitz 
        # It is the polynomial approximation in equation 35 in the paper called 
        # Thermodynamic and transport properties of Sodium Liquid and Vapor
        # [J/kg-K]
        # T   =   t_cool+273.15
        # c_p = 1.6582 - (8.4790*10^(-4))*T + (4.4541*10^(-7))*T.^2 - 2992.6*T.^(-2)
        # c_p =   1277
        R   =   therm_resist("cool","fuel")
        con =   (A_fuel*H_core)/(A_flow*2.0*u*R)*(T_f_o-t_cool_o)/(t_cool_o-T_in)
        c_p =   con/density_c(t_cool)
        return c_p

    def cp_mod(self):
        c_p = 100.0 # TODO : placeholder
        return c_p

    def cp_refl(self):
        c_p = 100.0 # TODO : placeholder
        return c_p

    def res(self, component1, component2):
        A = self.area(set(component1, component2))
        h = self.h(set(component1, component2))
        r_th = 1.0/h/A
        return r_th
    
    def area(self, components):
        if components == set("fuel", "cool"):
            return 4.0*math.pi*pow(self._pebble_r
        elif 

    # therm_resist calcualtes the termal resistance between the coolant and the
    # fuel.
    def therm_resist(self, t_fuel, t_cool):
    # con1    =   1/(2*pi*k_clad)*log(R_clad/R_fuel);
    # con2    =   1/(2*pi*R_clad*h_conv(T_c));
    # con3    =   w/(4*pi*conductivity_f(T_f));
    # R_th    =   A_fuel*(con1+con2+con3);


    def h_conv(self, t_cool):
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
        # TODO : placeholder : 
        return 27000

