import numpy as np

class State:

    def __init__(self):

    """A class representing the solution state, such as the initial conditions"""
    def T(self):
        """A function that returns the temperature vector, representing the 
        temperatures of each component"""


    def T(self, val):
        """A function that sets the temperature vector"""
        self.T = val

    def T(self, key, val):
        """A function that sets the temperature of a single component with the 
        key, key"""
        self.T[key] = val



