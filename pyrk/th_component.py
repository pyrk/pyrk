import numpy as np
from inp import validation
from utilities.ur import units
from timer import Timer
import math
from materials.material import Material


class THComponent(object):

    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal hydraulics sub block
    """

    def __init__(self, name=None,
                 mat=Material(),
                 vol=0.0*units.meter**3,
                 T0=0.0*units.kelvin,
                 alpha_temp=0*units.delta_k/units.kelvin,
                 timer=Timer(),
                 heatgen=False,
                 power_tot=0*units.watt,
                 sph=False,
                 ri=0*units.meter,
                 ro=0*units.meter):
        """Initalizes a thermal hydraulic component.
        A thermal-hydraulic component will be treated as one "lump" in the
        lumped capacitance model.

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param mat: The material of this component
        :type mat: Material object
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
        :param power_tot: power generated in this component
        :type power_tot: float
        :param sph: is this component a spherical component, spherical
        equations for heatgen, conduction are different,
        post-processing is different too
        :type sph: bool
        :param ri: inner radius of the sph/annular component, ri=0 for sphere
        :type ri: float
        :param ro: outer radius of the sph/annular component,
        ro=radius for sphere
        :type ro: float
        """
        self.name = name
        self.vol = vol.to('meter**3')
        self.mat = mat
        self.k = mat.k
        self.cp = mat.cp
        self.dm = mat.dm
        self.timer = timer
        self.T = units.Quantity(np.zeros(shape=(timer.timesteps(),),
                                         dtype=float), 'kelvin')
        self.T[0] = T0
        self.T0 = T0
        self.alpha_temp = alpha_temp.to('delta_k/kelvin')
        self.heatgen = heatgen
        self.power_tot = power_tot
        self.cond = {}
        self.conv = {}
        self.adv = {}
        self.mass = {}
        self.cust = {}
        self.prev_t_idx = 0
        self.convBC = {}
        self.sph = sph
        self.ri = ri.to('meter')
        self.ro = ro.to('meter')

    def mesh(self, size):
        '''cut a THComponent into a list of smaller components
        uniform meshing method, only implemented for spherical components

        :param size: size of uniform mesh element
        :type size: float with length unit
        :return: list of smaller components
        '''
        if not self.sph:
            msg = 'mesh function only implemented for spherical component'
            raise TypeError(msg)
        if size > self.ro-self.ri:
            msg = 'mesh size can not be larger than the thickness of the shell'
            raise ValueError(msg)
        N = int(round((self.ro-self.ri)/size))
        to_ret = []
        for i in range(0, N):
            ri = self.ri+i*size
            ro = self.ri+(i+1)*size
            vol = 4.0/3.0*math.pi*(ro**3-ri**3)
            power_tot = self.power_tot/self.vol*vol
            alpha_temp = self.alpha_temp/self.vol*vol
            to_ret.append(THComponent(name=self.name+'%d' % i,
                                      mat=self.mat,
                                      vol=vol,
                                      T0=self.T0,
                                      alpha_temp=alpha_temp,
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
        :param temp: the new temperature
        :type float: float, units of kelvin
        """
        self.T[timestep] = temp
        self.prev_t_idx = timestep
        return self.T[timestep]

    def dtemp(self, timestep):
        """calculate temperature difference between the given timestep and the
        timestep where feedback is turned on

        :param timestep: the timestep at which to query the tempareture
        :type timestep: int
        """
        T0 = self.T[self.timer.t_idx_feedback]
        # timestep -1 because timestep hasn't been updated yet, is 0
        return self.T[timestep-1]-T0

    def temp_reactivity(self, timestep):
        '''calculate reactivity of a component from temperature feedback

        :param timestep: the timestep at which to calculate reactivity feedback
        :type timestep: int
        :param T0_timestep: the timestep at which the temperature is used as
        reference temperature
        :type T0_timestep: int
        '''
        assert timestep > self.timer.t_idx_feedback, "timestep that feedback\
            starts %f should be prior to the timestep %f for temp feedback\
            calculation" % (self.timer.t_idx_feedback, timestep)
        return self.alpha_temp*self.dtemp(timestep)

    def add_convection(self, env, h, area):
        '''add convection in the self.conv dictionary

        :param env: name of the component that heat is transfered to/from
        :type env: str
        :param h: heat transfer coefficient
        :type h: float
        :param area: heat transfer area
        :type area: float
        '''
        self.conv[env] = {
            "h": h.to('joule/second/kelvin/meter**2'),
            "area": area
        }

    def add_mass_trans(self, env, H, u):
        self.mass[env] = {"H": H,
                          "u": u}

    def add_custom(self, env, res):
        self.cust[env] = {"res": res.to(units.kelvin/units.watt)}

    def addConvBC(self, env, prev_comp, h, R):
        '''add convective boundary condition

        :param env: name of the environment for convective heat transfer
        (the fluid)
        :type env: str
        :param prev_comp: name of the component that is immediately inside the
        boundary component
        :type prev_comp: str
        :param h: convective heat transfer coefficient
        :type h: float
        :param R: radius of the sphere
        :type R: float
        '''
        self.convBC[env] = {
            "h": h.to('joule/second/kelvin/meter**2'),
            "prev_comp": prev_comp,
            "R": R
        }

    def add_conduction(self, env, area=0.0*units.meter**2, L=0.0*units.meter,
                       r_b=0.0*units.meter, r_env=0.0*units.meter):
        '''Add parameters for conduction heat transfer calculation
        area and L are used for slab geometry
        r_b and r_env are used for spherical heat diffusion

        :param env: name of the component that this component conduct heat to
        :type env: str
        :param area: conduction surface for the slab
        :type area: float
        :param L: thickness of the slab
        :type L: float
        :param r_b: outer radius of the component
        :type r_b: float
        :param r_env: outer radius of the environment
        :type r_env: float
        '''
        self.cond[env] = {
            "area": area.to('meter**2'),
            "L": L.to('meter'),
            "r_b": r_b.to('meter'),
            "r_env": r_env.to('meter')
        }

    def add_advection(self, name, m_flow, t_in, cp):
        '''Add advection dictionary to the fluid component(coolant) that has
        advective heat tranfer

        :param m_flow: mass flow rate
        :type m_flow: float
        :param t_in: temperature at the inlet of the control volume
        :type t_in: float
        :param cp: specific heat capacity
        :type cp: float
        '''
        self.adv[name] = {
            "m_flow": m_flow.to('kg/second'),
            "t_in": t_in.to('kelvin'),
            "cp": cp.to('joule/kg/kelvin')
        }


class THSuperComponent(THComponent):

    '''A 'component' containing a list of component
    Creating a superComponent would automatically define conduction between the
    mesh elements'''

    def __init__(self, name, T0, sub_comp=[], timer=Timer()):
        """Initalizes a thermal hydraulic super component.

        :param name: The name of the supercomponent (i.e., "fuel" or "cool")
        :type name: str.
        :param T0: The initial temperature of the supercomponent
        :type T0: float.
        :param sub_comp: List of components that makes up the supercomponent.
        The sub_components should be in order from the center to the outside
        :type sub_comp: list of THComponent
        :param timer: The timer instance for the sim
        :type timer: Timer object
        """
        THComponent.__init__(self, name=name,
                             mat=Material(),
                             vol=0.0*units.meter**3,
                             T0=T0,
                             alpha_temp=0*units.delta_k/units.kelvin,
                             timer=timer,
                             heatgen=False,
                             power_tot=0*units.watt,
                             sph=False,
                             ri=0*units.meter,
                             ro=0*units.meter)
        self.sub_comp = sub_comp
        self.T = units.Quantity(np.zeros(shape=(timer.timesteps(),),
                                         dtype=float), 'kelvin')
        self.T[0] = T0
        self.conv = {}
        self.add_conduction_in_mesh()
        self.alpha_temp = 0.0*units.delta_k/units.kelvin

    def compute_tr(self, t_env, t_innercomp):
        '''compute temperature at r=R for the sphere from the temperature at r=R-dr
        and the temperature of the env/fluid/coolant

        :param t_env: temperature of the component(env) that self tranfers
        heat with
        :type t_env: float
        :param t_innercomp: temperature of the component that is inside self
        :type t_innercomp: float
        '''
        for envname, d in self.conv.iteritems():
            h = self.conv[envname]["h"].magnitude
            k = self.conv[envname]["k"].magnitude
            dr = self.conv[envname]["dr"].magnitude
        return (-h/k*t_env+t_innercomp/dr)/(1/dr-h/k)

    def add_component(self, a_component):
        self.sub_comp.append(a_component)

    def add_conv_bc(self, envname, h):
        '''add convective boundary condition to the supercomponent

        :param envname: the name of the component that self tranfer heat with
        :type envname: str
        :param h: convective heat transfer coefficient
        :type h: float
        '''
        self.sub_comp[-2].addConvBC(envname,
                                    self.sub_comp[-1],
                                    h,
                                    (self.sub_comp)[-1].ro)
        self.conv[envname] = {'h': h,
                              'k': self.sub_comp[-1].k,
                              'dr': self.sub_comp[-1].ro-self.sub_comp[-1].ri
                              }

    def add_conduction_in_mesh(self):
        '''add conduction between the mesh elements
        '''
        N = len(self.sub_comp)
        # element i=0:
        self.sub_comp[0].add_conduction(
            self.sub_comp[1].name)
        # element i=1:elementNb-3
        for i in range(1, N-2):
            self.sub_comp[i].add_conduction(
                self.sub_comp[i - 1].name)
            self.sub_comp[i].add_conduction(
                self.sub_comp[i + 1].name)
        # element i=elementNb-2
        self.sub_comp[N - 2].add_conduction(
            self.sub_comp[N - 3].name)
