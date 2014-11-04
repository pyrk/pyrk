from scipy import integrate
import th_params

class ThermalHydraulics(object):
    """This class handles calculations and data related to the 
    thermal_hydraulics subblock
    """

    def __init__(self):
        self._params = th_params.THParams()

    def dtempdt(self, component, temps, power, omegas, component_names):
        tfuel = temps[component_names["fuel"]]
        tcool = temps[component_names["cool"]]
        tmod = temps[component_names["mod"]]
        trefl = temps[component_names["refl"]]
        if component == "fuel":
            return self.dtempfueldt(power, omegas, tfuel, tcool, tmod)
        elif component == "cool":
            return self.dtempcooldt(tfuel, tcool)
        elif component == "mod":
            return self.dtempmoddt(tfuel, tmod)
        elif component == "refl":
            return self.dtemprefldt(tfuel, trefl)
        else :
            raise KeyError("This work only supports fuel, cool, mod, and \
                    refl keys")
    
    def dtempfueldt(self, power, omegas, tfuel, tcool, tmod):
        # check this, it may not get things quite right... 
        rho = self._params.rho("fuel",tfuel)
        cp = self._params.cp("fuel")
        vol = self._params.vol("fuel")
        rm = self._params.r("mod")
        amod = self._params.area(set(["mod","fuel"]))
        afuel = self._params.area(set(["fuel","cool"]))
        kf = self._params.k("fuel",tfuel)
        hf = self._params.h("fuel")
        power_tot = self._params._power_tot
        #heat_gen = (power_tot/vol/rho/cp)*((1-self._params._kappa)*power + sum(omegas)) 
        heat_gen = (power_tot)*(power-sum(omegas)) 
        cond_mod = self.conduction(tfuel, tmod, rm, kf, amod)
        conv_cool = self.convection(tfuel, tcool, hf, afuel)
        return (heat_gen - cond_mod - conv_cool)/(rho*cp*vol)

    def dtempcooldt(self, tfuel, tcool):
        h = self._params._core_height
        tinlet = self._params._t_inlet
        v = self._params._vel_cool
        rho = self._params.rho("cool", tcool)
        cp = self._params.cp("cool")
        res = self._params.res("cool", "fuel")
        convection = (2.0*v/h)*(tcool-tinlet) 
        afuel = self._params.area(set(["fuel", "cool"])) # this is one pebble?
        aflow = self._params.flow_area() # this is the flow path cross section
        conduction = (afuel/aflow)*(tfuel - tcool)/(rho*cp*res)
        return conduction - convection 

    def dtempmoddt(self, tfuel, tmod):
        rho = self._params.rho("mod", tmod)
        cp = self._params.cp("mod")
        res_m = self._params.res("mod", "fuel")
        f = (tmod-tfuel)/(rho*cp*res_m)
        return f

    def dtemprefldt(self, tcool, trefl):
        rho = self._params.rho("refl", trefl)
        cp = self._params.cp("refl")
        res_m = self._params.res("refl", "cool")
        f = (trefl - tcool)/(rho*cp*res_m)
        return f

    def convection(self, t_b, t_env, h, A):
        """
        The temperature of the body, environment, the heat transfer 
        coefficient, and the surface area of heat transfer are required.
        """
        num = (t_b-t_env)
        denom = (h*A)
        return num/denom

    def conduction(self, t_b, t_env, L, k, A):
        """
        The temperature of the body, environment, the length scale, the thermal 
        conductivity, and the surface area of heat transfer are required.
        """
        num = L*(t_b-t_env)
        denom = (k*A)
        return num/denom


