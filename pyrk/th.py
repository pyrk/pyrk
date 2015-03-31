import numpy as np
from inp import validation
from ur import units


class THComponent(object):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal_hydraulics subblock
    """

    def __init__(self, name, vol=0, k=0, dm=None, T0=0, timesteps=0):
        """Initalizes a thermal hydraulic component.
        A thermal-hydraulic component will be treated as one "lump" in the
        lumped capacitance model.

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param vol: The volume of the component
        :param k: The thermal conductivity of the component
        :type k: float.
        :param dm: The density of the component
        :type dm: DensityModel object
        :param T0: The initial temperature of the component
        :type T0: float.
        :param timesteps: The number of timesteps in this simulation
        :type timesteps: int
        """
        self.name = name
        self.vol = vol
        validation.validate_ge("vol", vol, 0*units.meter**3)
        self.k = k
        validation.validate_ge("k", k, 0*units.watt/units.meter/units.kelvin)
        self.dm = dm
        self.T0 = T0
        self.T = units.Quantity(np.zeros(shape=(1, timesteps),
                                         dtype=float), 'kelvin')
        self.T[0] = T0
        self.timesteps = timesteps

    def temp(self, timestep):
        """The temperature of this component at the chosen timestep
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :return: the temperature of the component at the chosen timestep
        :rtype: float, in units of kelvin
        """
        validation.validate_ge("timestep", timestep, 0)
        validation.validate_le("timestep", timestep, self.timesteps)
        return self.T[0, timestep]

    def rho(self, timestep):
        """<+description+>
        :param <++>: <++>
        :type <++>: <++>
        :param <++>: <++>
        :type <++>: <++>
        :param <++>: <++>
        :type <++>: <++>
        """
        ret = self.dm.rho(self.temp(timestep))
        return ret

    def update_temp(self, timestep, dtempdt):
        """Updates the temperature
        :param <++>: <++>
        :type <++>: <++>
        :param <++>: <++>
        :type <++>: <++>
        :param <++>: <++>
        :type <++>: <++>
        """
        self.T[0, timestep] = self.T[0, timestep-1] + dtempdt
        return self.T[0, timestep]
