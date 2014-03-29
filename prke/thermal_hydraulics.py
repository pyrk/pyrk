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

    def dtempdt(self, component, temps, power):
        if component == "fuel":
            return self.dtempfueldt(power, temps["cool"], temps["mod"])
        elif component == "cool":
            return self.dtempcooldt(temps["fuel"])
        elif component == "mod":
            return self.dtempmoddt(temps["cool"])
        elif component == "refl":
            return self.dtemprefldt(temps["fuel"])
        else :
            raise KeyError("This work only supports fuel, cool, mod, and \
                    refl keys")


    def dtempmoddt(self, tfuel):
        h = self._params.h("mod")
        # TODO Replace. This is a lie 
        f = h*(tfuel)
        return f
    
    def dtempfueldt(self, power, tcool, tmod):
        h = self._params.h("cool")
        # TODO Replace. This is a lie 
        f = h*(tcool - tmod) 
        return f

    def dtempcooldt(self, tfuel):
        h = self._params.h("refl")
        # TODO Replace. This is a lie 
        f = h*(tfuel)
        return f

    def dtemprefldt(self, tcool):
        h = self._params.h("cool")
        # TODO Replace. This is a lie 
        f = h*(tcool)
        return f
