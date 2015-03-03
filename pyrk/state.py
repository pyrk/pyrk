import numpy as np

class State(object):
    """A class representing the solution state, such as the initial conditions"""

    def __init__(self, alphas, temps):
        """Initializes the State"""
        self._alpha = {"fuel": -3.8,
                "cool": -1.8,
                "gmod": -0.7,
                "refl": 1.8
                }
        self._temp = {"fuel": 730.,
                "cool": 650.,
                "gmod": 700.,
                "refl": 650.
                }
        self._t
        self._dt

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

    def rho(self):
        """A function that returns the reactivity dictionary, representing the
        reactivities of each component"""
        return self._rho_temp

    def rho(self, rho_dict):
        """A functi:on that sets the reactivity dictionary"""
        self._rho_temp = rho_dict

    def rho(self, key, val):
        """A function that sets the reactivity of a single component with the
        key, key"""
        self._rho[key] = val

    def power(self):
        """A function that returns the power of the reactor"""
        return self._power

    def power(self, val):
        self._power = val

    def dydt(self):
        for key in elements :
            lhs[key] = self.rhs[key]()
        return lhs

    def neutronics(self):
        """This performs the neutronics subblock calculation"""


    def thermal_hydraulics(self):
        """This performas the thermal hydraulics subblock calculation"""


class Coolant(object):
    def __init__(self):
        self._density
        self._spec_heat
        self._kth
        self._vis

