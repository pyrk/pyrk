import numpy as np
from inp import validation
from ur import units
from density_model import DensityModel
from timer import Timer
from material import Material
import math

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
                 power_tot=0*units.watt,
                 sph=False,
                 ri=0*units.meter,
                 ro=0*units.meter
                 ):
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
        :param adv: is this component losses heat from advection
        :type adv: bool
        :param advheat: heat transfered through advection(watts), positive if
        gain heat, negative is loss heat
        :param sph: is this component a spherical component, spherical equations
        for heatgen, conduction are different, post-processing is different too
        :type sph: bool
        :param ri and ro: inner radius and outer radius of the sph/annular component
        """
        self.name = name
        self.vol = vol.to('meter**3')
        validation.validate_ge("vol", vol, 0*units.meter**3)
        self.mat = mat
        self.k = mat.k
        self.cp = mat.cp
        self.dm = mat.dm
        self.name = name
        self.timer = timer
        self.T0 = T0.to('kelvin')
        validation.validate_num("T", T0)
        self.T = units.Quantity(np.zeros(shape=(timer.timesteps(),),
                                         dtype=float), 'kelvin')
        self.T[0] = T0
        self.alpha_temp = alpha_temp.to('delta_k/kelvin')
        self.heatgen = heatgen
        self.power_tot = power_tot
        self.cond = {}
        self.conv = {}
        self.adv = {}
        self.prev_t_idx = 0
        self.convBC = {}
        self.sph = sph
        self.ri = ri
        self.ro = ro

    def mesh(self, size):
        '''cut a THComponent into a list of smaller component'''
        N = int(round((self.ro-self.ri)/size.to('meter')))
        #todo implement: assert (N*size).magnitude == (self.ro-self.ri).magnitude
        to_ret = []
        for i in range(0, N):
            ri = self.ri+i*size
            ro = self.ri+(i+1)*size
            vol = 4.0/3.0*math.pi*(ro**3-ri**3)
            power_tot = self.power_tot/self.vol*vol
            to_ret.append(THComponent(name=self.name+'%d'%i,
                                      mat=self.mat,
                                      vol=vol,
                                      T0=self.T0,
                                      alpha_temp=self.alpha_temp,
                                      timer=self.timer,
                                      heatgen=self.heatgen,
                                      power_tot=power_tot,
                                      sph=self.sph,
                                      ri=ri, ro=ro))
        return to_ret

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

    def addConvBC(self, env, prev_comp, h, R):
        self.convBC[env] = {
            "h": h.to('joule/second/kelvin/meter**2'),
            "prev_comp": prev_comp
            }

    def add_conduction(self, env, k, area=0.0*units.meter**2, L=0.0*units.meter,
                       r_b=0.0*units.meter, r_env=0.0*units.meter):
        self.cond[env] = {
            "k": k.to('watts/meter/kelvin'),
            "area": area.to('meter**2'),
            "L": L.to('meter'),
            "r_b": r_b.to('meter'),
            "r_env": r_env.to('meter')
        }

    def add_advection(self, name, m_flow, t_in, cp):
        self.adv[name] = {
            "m_flow": m_flow.to('kg/second'),
            "t_in": t_in.to('kelvin'),
            "cp": cp.to('joule/kg/kelvin')
        }


class THSuperComponent(object):

    '''A component containing a list of component'''

    def __init__(self, name, T0, sub_comp=[], timer=Timer()):
        self.sub_comp = sub_comp
        self.name = name
        # for a super component, T is the outer surface temperature
        self.timer = timer
        self.T0 = T0.to('kelvin')
        validation.validate_num("T", T0)
        self.T = units.Quantity(np.zeros(shape=(timer.timesteps(),),
                                         dtype=float), 'kelvin')
        self.T[0] = T0

    def update_temp_R(self, timestep, t_env, t_r):
        """Updates the temperature
        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :param temp: the new tempterature
        :type float: float, units of kelvin
        """
        #TODO: this is very bad, need to be changed
        h=4700.0*units.watts/units.kelvin/units.meter**2
        k=15.0*units.watts/units.meter/units.kelvin
        dr=self.sub_comp[0].ro-self.sub_comp[0].ri
        self.T[timestep] = (-h/k*t_env+t_r/dr)/(1/dr-h/k)
        self.prev_t_idx = timestep
        return self.T[timestep]

    def add_component(self, a_component):
        self.sub_comp.append(a_component)

    def add_conv_bc(self, envname, h):
        self.sub_comp[-2].addConvBC(envname,
                                   self.sub_comp[-1],
                                   h,
                                   (self.sub_comp)[-1].ro)
    def add_conduction_in_mesh(self):
        N = len(self.sub_comp)
        # element i=0:
        self.sub_comp[0].add_conduction(self.sub_comp[1].name, self.sub_comp[1].k)
        # element i=1:elementNb-3
        for i in range(1, N-3):
            self.sub_comp[i].add_conduction(self.sub_comp[i-1].name, self.sub_comp[i].k)
            self.sub_comp[i].add_conduction(self.sub_comp[i+1].name, self.sub_comp[i].k)
        # element i=elementNb-2
        self.sub_comp[N-2].add_conduction(self.sub_comp[N-3].name, self.sub_comp[N-2].k)
