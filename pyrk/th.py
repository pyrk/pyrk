import numpy as np
from inp import validation
from ur import units


class THComponent(object):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal_hydraulics subblock
    """

    def __init__(self, name, vol=0, k=0, dm=None, T0=0, si=None):
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
        :param si: The simulation info object for this simulation
        :type si: SimInfo object
        """
        self.name = name
        self.vol = vol
        validation.validate_ge("vol", vol, 0*units.meter**3)
        self.k = k
        validation.validate_ge("k", k, 0*units.watt/units.meter/units.kelvin)
        self.dm = dm
        self.T0 = T0
        self.T = units.Quantity(np.zeros(shape=(1, si.timesteps()),
                                         dtype=float), 'kelvin')
        self.T[0] = T0
        self.sim_info = si

    def temp(self, timestep):
        validation.validate_ge("timestep", timestep, 0)
        validation.validate_le("timestep", timestep, self.sim_info.timesteps())
        return self.T[0, timestep]

    def rho(self, timestep):
        ret = self.dm.rho(self.temp(timestep))
        return ret

    def update_temp(self, timestep, dtempdt):
        self.T[0, timestep] = self.T[0, timestep-1] + dtempdt
        return self.T[0, timestep]
