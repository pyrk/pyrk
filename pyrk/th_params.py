import math


def vol_sphere(r):
    assert(r >= 0)
    return (4./3.)*math.pi*pow(r, 3)


class THParams(object):
    """This holds the parameters for the PB-FHR."""

    def __init__(self):
        self._components = {"fuel": 0, "cool": 1, "mod": 2, "refl": 3}
        # below from greenspan/cisneros
        self._init_temps = {
            "fuel": 730.0 + 273.15,
            "cool": 650.0 + 273.15,
            "mod": 700.0 + 273.15,
            "refl": 650.0 + 273.15
            }
        # the data below comes from design doc rev c
        self._power_tot = 236000.0  # Wth
        self._vol_tot_active = 4.16  # m^3
        self._vol_tot_defuel = 1.03  # m^3
        self._vol_tot_refl = 4.8  # m^3
        self._pebble_porosity = 0.4  # [-]
        # self._vol_flow_rate = 976.0*0.3 # kg/s TODO 0.3 is nat circ guess
        self._vel_cool = 2.  # m/s
        self._t_inlet = 600.0
        # [m] ... matrix(4mm) + coating(1mm)
        self._thickness_fuel_matrix = 0.005
        self._r_fuel = 0.03  # [m] ... matrix(4mm) + coating(1mm)
        self._r_mod = 0.025
        self._pebble_r = self._r_fuel + self._r_mod
        self._kappa = 0.06  # TODO if you fix omegas, kappa ~ 0.06
        self._core_height = 3.5  # [m] APPROXIMATELY (TODO look for actual)
        self._core_inner_radius = 0.35  # m
        self._core_outer_radius = 1.25  # m

    def flow_area(self):
        inner = 2.0*math.pi*pow(self._core_inner_radius, 2)
        outer = 2.0*math.pi*pow(self._core_outer_radius, 2)
        return outer - inner

    def r(self, component):
        """Radius of each component in m"""
        if component == "fuel":
            return self._r_fuel
        elif component == "mod":
            return self._r_mod
        else:
            raise KeyError("The only supported options for components with \
                           radii are fuel and mod.")

    def vol(self, component):
        f = self._r_fuel
        m = self._r_mod
        tot_fuel_pebble_vol = (1 - self._pebble_porosity) *\
            (self._vol_tot_active + self._vol_tot_defuel)
        single_pebble_vol = vol_sphere(f)
        if component == "fuel":
            fuel_vol_in_single_pebble = vol_sphere(f+m) - vol_sphere(m)
            fuel_vol = tot_fuel_pebble_vol * \
                fuel_vol_in_single_pebble/single_pebble_vol
            return fuel_vol
        elif component == "cool":
            tot_vol = self._vol_tot_active + self._vol_tot_defuel + \
                self._vol_tot_refl
            return tot_vol*self._pebble_porosity
        elif component == "mod":
            mod_vol_in_single_pebble = vol_sphere(m)
            mod_vol = tot_fuel_pebble_vol * \
                mod_vol_in_single_pebble/single_pebble_vol
            return mod_vol
        elif component == "refl":
            return (1 - self._pebble_porosity)*self._vol_tot_refl
        else:
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")

    # Conductivity
    def k(self, component, temp):
        """Thermal conductivitiy in W/m-K"""
        if component == "fuel":
            return self.k_fuel(temp)
        elif component == "cool":
            return self.k_cool(temp)
        elif component == "mod":
            return self.k_graphite(temp)
        elif component == "refl":
            return self.k_graphite(temp)
        else:
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")

    def k_cool(self, t_cool):
        """Thermal conductivitiy in W/m-K for flibe"""
        # http://www.psfc.mit.edu/library1/catalog/reports/1980/80rr
        # /80rr012/80rr012_full.pdf
        # would prefer temperature dependent thermal conductivity?
        # [W/m-K]
        return 1.0

    def k_fuel(self, t_fuel):
        """Thermal conductivitiy in W/m-K for the triso fuel layer"""
        # [W/m-K]
        # in the pbmr, they use zehner-schlunder to approximate k_eff for the
        # pebble bed:
        # http://www.sciencedirect.com/science/article/pii/S0029549306000185
        # here is a paper on that approximation:
        # http://ac.els-cdn.com/0017931094903921/1-s2.0-0017931094903921-main.pdf
        # ?_tid=e7d08bac-b380-11e3-90e0-00000aacb35f&acdnat
        # =1395685377_d73165eba81bc145ccebc98c195abf36
        k = 2
        # 20 is what's assumed for the pbmr pebble bed...
        return k

    def k_graphite(self, t_graphite):
        """Thermal conductivitiy in W/m-K for the graphite moderator and the \
        reflector"""
        return 0.26

    def rho(self, component, temp):
        """Density, as a function of temperature [kg/m^3]"""
        # SHOULD THIS BE IN GRAMS?
        if component == "fuel":
            return self.rho_fuel(temp)
        elif component == "cool":
            return self.rho_cool(temp)
        elif component == "mod":
            return self.rho_graphite(temp)
        elif component == "refl":
            return self.rho_graphite(temp)
        else:
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
        # t_m = 732.2
        # critical point [K]
        # t_c = 4498.8
        # rho correlation [kg/m^3]
        rho = 2415.6 - 0.49072*t_cool
        # at 650C, this is 1962
        return rho

    def rho_fuel(self, t_fuel):
        # [kg/m^3]
        rho = 1720.0  # from COMSOL model by Raluca Scarlat
        return rho

    def rho_graphite(self, t_graphite):
        rho = 100
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
        else:
            raise KeyError("The only supported options for components are fuel, \
            cool, mod, and refl.")

    def cp_fuel(self):
        # [J/kg-K]
        c_p = 1744  # From COMSOL model by Raluca Scarlat
        return c_p

    def cp_cool(self):
        # [J/kg-K]
        return 2350.0  # from www-ferp.ucsd.edu/LIB/PROPS/HTS.shtml

    def cp_mod(self):
        c_p = 1650.0
        # Approximate:
        # http://www.sciencedirect.com/science/article/pii/0022369760900950
        return c_p

    def cp_refl(self):
        c_p = 1650.0
        # Approximate:
        # http://www.sciencedirect.com/science/article/pii/0022369760900950
        return c_p

    def res(self, component1, component2):
        A = self.area(set([component1, component2]))
        h = self.h(set([component1, component2]))
        r_th = 1.0/h/A
        return r_th

    def area(self, components):
        if components == set(["mod", "fuel"]):
            return 4.0*math.pi*pow(self._r_mod, 2)
        elif components == set(["fuel", "cool"]):
            return 4.0*math.pi*pow(self._pebble_r, 2)
        elif components == set(["cool", "refl"]):
            return 2*math.pi*self._core_height
        else:
            raise KeyError("The only supported options for component set are \
            the pairs mod&fuel, fuel&cool, cool&refl")

    def h(self, components):
        # h_conv calculates the heat tranfer coefficient between the coolant
        # the fuel.
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
        return 4700
