import numpy as np
from inp import validation
from ur import units


class THComponent(object):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal_hydraulics subblock
    """

    def __init__(self, name=None, vol=0, k=0, cp=0, dm=None, T0=0,
                 alpha_temp=0, timesteps=0, heatgen=False):
        """Initalizes a thermal hydraulic component.
        A thermal-hydraulic component will be treated as one "lump" in the
        lumped capacitance model.

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param vol: The volume of the component
        :param k: The thermal conductivity of the component
        :type k: float.
        :param cp: specific heat capacity, $c_p$, in units of $J/kg-K$
        :type cp: float, in units of $J/kg-K$
        :param <++>: <++>
        :type <++>: <++>
        :param dm: The density of the component
        :type dm: DensityModel object
        :param T0: The initial temperature of the component
        :type T0: float.
        :param alpha_temp: temperature coefficient of reactivity
        :type alpha_temp: float
        :param timesteps: The number of timesteps in this simulation
        :type timesteps: int
        :param heatgen: is this component a heat generator (fuel)
        :type heatgen: bool
        """
        self.name = name
        self.vol = vol
        validation.validate_ge("vol", vol, 0*units.meter**3)
        self.k = k
        validation.validate_ge("k", k, 0*units.watt/units.meter/units.kelvin)
        self.dm = dm
        self.T0 = T0
        self.T = units.Quantity(np.zeros(shape=(timesteps), dtype=float),
                                'kelvin')
        self.T[0] = T0
        self.alpha_temp = alpha_temp.to('delta_k/kelvin')
        self.timesteps = timesteps
        self.heatgen = heatgen

    def temp(self, timestep):
        """The temperature of this component at the chosen timestep
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :return: the temperature of the component at the chosen timestep
        :rtype: float, in units of kelvin
        """
        validation.validate_ge("timestep", timestep, 0)
        validation.validate_le("timestep", timestep, self.timesteps)
        return self.T[timestep]

    def rho(self, timestep):
        """The density of this component's materials
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :return: the density of this component
        :rtype: float, in units of $kg/m^3$
        """
        ret = self.dm.rho(self.temp(timestep))
        return ret

    def update_temp(self, timestep, dtempdt):
        """Updates the temperature
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :param dtempdt: the change in temperature since the last timestep
        :type float: float, units of kelvin
        """
        self.T[timestep] = self.T[timestep-1] + dtempdt
        return self.T[timestep]

    def dtempdt(self, t, dt):
        t_idx = int(t/dt)
        if t_idx == 0:
            prev = 0
        else:
            prev = t_idx - 1
        return (self.T[t_idx] - self.T[prev])

    def temp_reactivity(self, t, dt):
        return self.alpha_temp*self.dtempdt(t, dt)

    def add_convection(self, env=None, h, area):
        self.conv[env] = {"h":h, "area":area}

    def add_conduction(self, component=None, area):
        self.cond[env] = area
