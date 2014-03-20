import numpy as np
from geometry import Geometry

class State(object):
    """A class representing the solution state, such as the initial conditions"""

    def __init__(self):
        """Initializes the State"""
        self._temp
        self._rho_temp


    def temp(self):
        """A function that returns the temperature vector, representing the 
        temperatures of each component"""
        return self._temp


    def temp(self, val):
        """A function that sets the temperature vector"""
        self._temp = val

    def temp(self, key, val):
        """A function that sets the temperature of a single component with the 
        key, key"""
        self._temp[key] = val

    def rho_temp(self):
        """A function that returns the reactivity vector, representing the 
        reactivities of each component"""
        return self._rho_temp


    def rho_temp(self, val):
        """A functi:on that sets the reactivity vector"""
        self._rho_temp = val

    def rho_temp(self, key, val):
        """A function that sets the reactivity of a single component with the 
        key, key"""
        self._rho_temp[key] = val


class PrecursorData(object):
    def __init__(self, nuc, e):
        """initializes the precursor group data for the fissioning nuclide. e 
        should be 'thermal' or 'fast' to indicate the energy spectrum."""
        self._betas = betas()
        self._lambdas = lambdas()
        self._lambdas = omegas()
        self._lifetime = mean_lifetimes()
        self._nuc = nuc
        self._e = e
        nuc_options = {
                922350000 : u235,
                922380000 : pu238
                }
        e_options = {
                "thermal" : thermal,
                "fast" : fast
                }

        nuc_options[nuc]()
        e_options[e]()
        
    def betas(self):
        # obtained from http://arxiv.org/pdf/1001.4100.pdf
        beta_i["u235"]["thermal"] = []
        beta_i["u235"]["fast"] = [0.000266, 0.001491, 0.001316, 0.002849, 0.000896, 0.000182] 
        beta_i["pu239"]["thermal"] = [] 
        beta_i["pu239"]["fast"] = [] 

    def lambdas(self):
        # obtained from http://arxiv.org/pdf/1001.4100.pdf
        lambda_i["u235"]["thermal"] = []
        lambda_i["u235"]["fast"] = [0.0127, 0.0317, 0.155, 0.311, 1.4, 3.87] 
        lambda_i["pu239"]["thermal"] = [] 
        lambda_i["pu239"]["fast"] = []

    def omegas(self):
        # should obtain decay heat values
        omega_dict["u235"]["thermal"] = [0, 0, 0, 0, 0, 0]
        omega_dict["u235"]["fast"] = [0, 0, 0, 0, 0, 0]
        omega_dict["pu239"]["thermal"] = [] 
        omega_dict["pu239"]["fast"] = []

    def mean_lifetimes(self, nuc, e):
        lifetime_dict["u235"]["thermal"] = 1.08e-5 
        lifetime_dict["u235"]["fast"] = 0
        lifetime_dict["pu239"]["thermal"] = 0 
        lifetime_dict["pu239"]["fast"] = 0

class Coolant(object):
    def __init__(self):
        self._density
        self._spec_heat
        self._kth
        self._vis

