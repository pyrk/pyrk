from scipy import integrate
from th_params import *

class ThermalHydraulics(object):
    """This class handles calculations and data related to the 
    thermal_hydraulics subblock"""

    def __init__(self):
        self.check_keys(conductivities, spec_heat_caps)
        self._bodies = cond.keys()
        self._k = cond
        self._cp = spec_caps
            
    def check_keys(self, dict1, dict2):
        diff = set(dict1.keys) - set(dict2.keys)
        if len(diff) != 0:
            raise ValueError("The dictionaries of specific heat capacity and \
            conductivity have different keys. They must refer to the same set \
            of bodies")

    def rhs(self):
        for b in self._bodies:
            self._temp[key] = rhs(self._k[key], self._cp[key]) 
        
        for key in lhs.keys():
            if key in bodies:
                f = self.find_f(key)
        

    def find_f(self, key):
        try :
            self._f[key]
        except(KeyError): 
            raise KeyError("There is currently no defined function for the \
            temperature of the body: " + key)

    def temp(self, key):
        integrate.ode(f).set_integrator('dopri5')
        return self._t[key]


