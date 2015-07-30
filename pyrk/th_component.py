import numpy as np
from inp import validation
from utilities.ur import units
from density_model import DensityModel
from timer import Timer
from materials.material import Material

class THComponent(object):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal hydraulics subblock
    """

    def __init__(self, name=None,
                 mat=Material(),
                 vol=0*units.meter**3,
                 T0=0*units.kelvin,
                 alpha_temp=0*units.delta_k/units.kelvin,
                 timer=Timer(),
                 heatgen=False,
                 power_tot=0*units.watt):
        """Initalizes a thermal hydraulic component.
        A thermal-hydraulic component will be treated as one "lump" in the
        lumped capacitance model.

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param vol: The volume of the component
        :type vol: float meter**3
        :param T0: The initial temperature of the component
        :type T0: float.
        :param alpha_temp: temperature coefficient of reactivity
        :type alpha_temp: float
        :param timer: The timer instance for the sim
        :type timer: Timer object
        :param heatgen: is this component a heat generator (fuel)
        :type heatgen: bool
        """
        self.name = name
        self.vol = vol.to('meter**3')
        validation.validate_ge("vol", vol, 0*units.meter**3)
        self.k = mat.k
        self.cp = mat.cp
        self.dm = mat.dm
        self.T0 = T0.to('kelvin')
        validation.validate_num("T", T0)
        self.T = units.Quantity(np.zeros(shape=(timer.timesteps(),),
                                         dtype=float), 'kelvin')
        self.T[0] = T0
        self.alpha_temp = alpha_temp.to('delta_k/kelvin')
        self.timer = timer
        self.heatgen = heatgen
        self.power_tot = power_tot
        self.cond = {}
        self.conv = {}
        self.mass = {}
        self.cust = {}
        self.prev_t_idx = 0

    def temp(self, timestep):
        """The temperature of this component at the chosen timestep
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :return: the temperature of the component at the chosen timestep
        :rtype: float, in units of kelvin
        """
        validation.validate_ge("timestep", timestep, 0)
        validation.validate_le("timestep", timestep, self.timer.timesteps())
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

    def update_temp(self, timestep, temp):
        """Updates the temperature
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :param temp: the new tempterature
        :type float: float, units of kelvin
        """
        self.T[timestep] = temp
        self.prev_t_idx = timestep
        return self.T[timestep]

    def dtemp(self):
        if self.prev_t_idx == 0:
            return 0.0*units.kelvin
        else:
            return (self.T[self.prev_t_idx] - self.T[self.prev_t_idx-1])

    def temp_reactivity(self):
        return self.alpha_temp*self.dtemp()

    def add_convection(self, env, h, area):
        self.conv[env] = {
            "h": h.to('joule/second/kelvin/meter**2'),
            "area": area.to('meter**2')
        }

    def add_conduction(self, env, area):
        self.cond[env] = area.to('meter**2')

    def add_mass_trans(self, env, H, u):
        self.mass[env] = {"H": H,
                          "u": u}

    def add_custom(self, env, res):
        self.cust[env] = {"res": res.to(units.kelvin/units.watt)}
