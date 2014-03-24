import numpy as np
from geometry import Geometry

class State(object):
    """A class representing the solution state, such as the initial conditions"""

    def __init__(self):
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

class Coolant(object):
    def __init__(self):
        self._density
        self._spec_heat
        self._kth
        self._vis

