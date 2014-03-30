from scipy import integrate
import th_params

class ThermalHydraulics(object):
    """This class handles calculations and data related to the 
    thermal_hydraulics subblock"""

    def __init__(self):
        self._params = th_params.THParams()
        self._temps = self._params._init_temps

    def temp(self, component, t):
        return self._temps[component][t]

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
        #h = self._params.h("cool")
        # TODO Replace. This is a lie 
        f = power*(tfuel - tcool - tmod) 
        rho = self._params.rho("fuel")
        cp = self._params.cp("fuel")
        vol = self._params.vol("fuel")
        power_tot = self._params.power_tot()
        heat_gen = power_tot/vol/rho/cp
        (1-kappa)*power 
        return f

    def dtempcooldt(self, tfuel, tcool):
        #h = self._params.h("refl")
        # TODO Replace. This is a lie 
        f = (tfuel-tcool)
        return f

    def dtempmoddt(self, tfuel, tmod):
        #h = self._params.h("mod")
        # TODO Replace. This is a lie 
        f = (tfuel - tmod)
        return f

    def dtemprefldt(self, tcool, trefl):
        #h = self._params.h("cool")
        # TODO Replace. This is a lie 
        f = (tcool-trefl)
        return f
