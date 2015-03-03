import numpy as np
from inp import validation


class THComponent(object):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal_hydraulics subblock
    """

    def __init__(self, name, vol=0, k=0, rho=0, T0=0, si=None):
        """Initalizes a thermal hydraulic component

        Arguments
        ---------
        name : str
               The name of the component (a handle, like "fuel" or "cool")

        params : THParams object
                 An object containing the parameters for this function?

        """
        self.name = name
        self.vol = vol
        self.k = k
        self.rho = rho
        self.T0 = T0
        self.T = np.zeros(shape=(1, si.timesteps()), dtype=float)
        self.T[0] = T0
        self.sim_info = si

    def temp(self, timestep):
        validation.validate_ge("timestep", timestep, 0)
        validation.validate_le("timestep", timestep, si.timesteps())
        return self.T[timestep]
