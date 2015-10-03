import math
from th_component import THSuperComponent
from utilities.ur import units


class THSystem(object):

    """This class handles calculations and data related to the
    thermal hydraulics sub block
    """

    def __init__(self, kappa, components):
        self.kappa = kappa
        self.components = components

    def dtempdt(self, component, power, omegas, t_idx):
        to_ret = 0*units.kelvin/units.second
        cap = (component.rho(t_idx)*component.cp*component.vol)
        if component.heatgen:
            to_ret += self.heatgen(component, power, omegas)/cap
        for interface, area in component.cond.iteritems():
            env = self.comp_from_name(interface)
            to_ret -= self.conduction(t_b=component.T[t_idx],
                                      t_env=env.T[t_idx],
                                      k=component.k,
                                      L=component.vol/area,
                                      A=area)/cap
        for interface, d in component.conv.iteritems():
            env = self.comp_from_name(interface)
            to_ret -= self.convection(t_b=component.T[t_idx],
                                      t_env=env.T[t_idx],
                                      h=d['h'],
                                      A=d['area'])/cap
        for interface, d in component.mass.iteritems():
            env = self.comp_from_name(interface)
            to_ret -= self.mass_trans(t_b=component.T[t_idx],
                                      t_inlet=env.T[t_idx],
                                      H=d['H'],
                                      u=d['u'])
        for interface, d in component.cust.iteritems():
            env = self.comp_from_name(interface)
            to_ret -= self.custom(t_b=component.T[t_idx],
                                  t_env=env.T[t_idx],
                                  res=d['res'])/cap

        return to_ret.to('kelvin/second')

    def comp_from_name(self, name):
        """Returns the component with the matching name
        """
        for comp in self.components:
            if comp.name == name:
                return comp
        # uh oh, none was found
        msg = "There is no component with the name: "
        msg += name
        raise KeyError(msg)

    def heatgen(self, component, power, omegas):
        to_ret = (component.power_tot)*((1-self.kappa)*power + sum(omegas))
        return to_ret.to(units.watt)

    def mass_trans(self, t_b, t_inlet, H, u):
        """
        :param t_b: The temperature of the body
        :type t_b: float.
        :param t_inlet: The temperature of the flow inlet
        :type t_inlet:
        """
        num = 2.0*u*(t_b - t_inlet)
        denom = H
        return num/denom

    def convection(self, t_b, t_env, h, A):
        """
        :param t_b: The temperature of the body
        :type t_b: float.
        :param t_env: The temperature of the environment
        :type t_env: float.
        :param h: the heat transfer coefficient between environment and body
        :type h: float.
        :param A: the surface area of heat transfer
        :type A: float.
        """
        num = (t_b-t_env)
        denom = (1.0/(h*A))
        return num/denom

    def conduction(self, t_b, t_env, L, k, A):
        """
        :param t_b: The temperature of the body
        :type t_b: float.
        :param t_env: The temperature of the environment
        :type t_env: float.
        :param L: the length scale of the body
        :type L: float.
        :param k: the thermal conductivity
        :type k: float.
        :param A: the surface area of heat transfer
        :type A: float.
        """
        num = (t_b-t_env)
        denom = L/(k*A)
        return num/denom

    def custom(self, t_b, t_env, res):
        num = (t_b-t_env)
        denom = res.to(units.kelvin/units.watt)
        return num/denom


class THSystemSphPS(THSystem):

    """This class models heat transfer in a sphere with point heat source at the
    center and convective heat transfer between the sphere and liquid flow
    """

    def __init__(self, kappa, components):
        THSystem.__init__(self, kappa, components)

    def dtempdt(self, component, power, omegas, t_idx):
        to_ret = 0*units.kelvin/units.second
        cap = (component.rho(t_idx)*component.cp*component.vol)
        if component.heatgen:
            to_ret += self.heatgen(component, power, omegas)/cap
        for name, d in component.adv.iteritems():
            Qadv = self.advection(t_out=component.T[t_idx]*2.0 - d['t_in'],
                                  t_in=d['t_in'],
                                  m_flow=d['m_flow'],
                                  cp=d['cp'])
            to_ret -= Qadv/cap
            assert Qadv.magnitude >= 0, '''
            at step %d, %s is heating the system by %f watts???
            Tin is %f, Tout is %f, Tcomp is %f''' % (
                t_idx, component.name, Qadv.magnitude, d['t_in'].magnitude,
                (component.T[t_idx]*2 - d['t_in']).magnitude,
                component.T[t_idx].magnitude)
        for interface, d in component.cond.iteritems():
            env = self.comp_from_name(interface)
            Qcond = self.conduction(t_b=component.T[t_idx],
                                    t_env=env.T[t_idx],
                                    r_b=d['r_b'],
                                    r_env=d['r_env'],
                                    k=d['k'])
            to_ret -= Qcond/cap
            assert (Qcond*(component.T[t_idx]-env.T[t_idx])).magnitude >= 0, \
                'conduction from %s to %s, from temp %f to %f is wrong %f' % (
                    component.name, env.name, component.T[t_idx].magnitude,
                    env.T[t_idx].magnitude, Qcond.magnitude)
        for interface, d in component.conv.iteritems():
            env = self.comp_from_name(interface)
            Qconv = self.convection(t_b=component.T[t_idx],
                                    t_env=env.T[t_idx],
                                    h=d['h'],
                                    A=d['area'])
            to_ret -= Qconv/cap
            assert (Qconv*(component.T[t_idx]-env.T[t_idx])).magnitude >= 0,\
                'convection from %s to %s, from temp %f to %f is wrong %f' % (
                    component.name, env.name, component.T[t_idx].magnitude,
                    env.T[t_idx].magnitude, Qconv.magnitude)
        return to_ret

    def conduction(self, t_b, t_env, r_b, r_env, k):
        """
        heat transfer by conduction(watts)
        :param t_b: The temperature of the body
        :type t_b: float.
        :param t_env: The temperature of the environment
        :type t_env: float.
        :param r_b: The radius of body
        :type r_b: float.
        :param r_env: The radius of environment
        :type r_env: float.
        :param k: the thermal conductivity
        :type k: float.
        """
        num = 4*math.pi*k*(t_b-t_env)
        denom = (1/r_b - 1/r_env)
        return num/denom

    def advection(self, t_out, t_in, m_flow, cp):
        ''' calculate heat transfer by advection in watts
        :param t_out: outlet temperature
        :type t_out: float
        :param t_in: inlet temperature
        :type t_in: float
        :param m_flow: mass flow rate though the control volume
        :type m_flow: float
        :param cp: specific heat capacity of the fluid
        :type cp: float
        '''
        if t_out > t_in:
            return m_flow*cp*(t_out-t_in)
        else:
            return 0*units.watts


class THSystemSphFVM(THSystem):

    """This class models
    - 1-D heat diffusion in spherical geometry, for heat
    generation at any radius in the sphere,
    - advective heat transfer by fluid
    - convective heat transfer at the solid surface to fluid.
    """

    def __init__(self, kappa, components):
        THSystem.__init__(self, kappa, components)

    def dtempdt(self, component, power, omegas, t_idx):
        '''compute the derivative dtemperature/dt

        :param component: name of the component that dtemp/dt is calculated
        :type component: str
        :param power: nuclear power density
        :type power: float
        :param omegas: decay heat nuclear data?
        :type omegas: list?
        :param t_idx: the timestep that dtempdt is calculated for
        :type t_idx: int
        :return: value of dtemp/dt
        :rtype: float, kelvin/s
        '''
        to_ret = 0.0
        if isinstance(component, THSuperComponent):
            #  return 0 for superComponent, doesn't calculate the temperature
            #  variation of superComponent
            return to_ret*units.kelvin/units.second
        else:
            cap = (component.rho(t_idx).magnitude*component.cp.magnitude)
            if component.sph and component.ri.magnitude == 0.0:
                Qcent = self.BC_center(component, t_idx)
                to_ret -= Qcent/cap
            for interface, d in component.convBC.iteritems():
                env = self.comp_from_name(interface)
                QconvBC = self.convBoundary(component,
                                            t_b=component.T[t_idx].magnitude,
                                            t_env=env.T[t_idx].magnitude,
                                            h=d["h"],
                                            R=d["R"])
                to_ret -= QconvBC/cap
            if component.heatgen:
                to_ret += self.heatgenFVM(component, power, omegas)/cap
            for interface, d in component.cond.iteritems():
                env = self.comp_from_name(interface)
                Qcond = self.conductionFVM(component, env, t_idx)
                to_ret -= Qcond/cap
            for interface, d in component.conv.iteritems():
                env = self.comp_from_name(interface)
                if isinstance(env, THSuperComponent):
                    Tr = env.compute_tr(component.T[t_idx].magnitude,
                                        env.sub_comp[-2].T[t_idx].magnitude)
                    Qconv = self.convection(t_b=component.T[t_idx].magnitude,
                                            t_env=Tr,
                                            h=d['h'],
                                            A=d['area'])
                    assert (Qconv*(component.T[t_idx].magnitude-Tr)) >= 0, '''
                    convection from %s to %s, from low temperature %f to
                    high temperature %f is wrong: %f''' % (
                        component.name, env.name, component.T[t_idx].magnitude,
                        Tr, Qconv.magnitude)
                else:
                    Qconv = self.convection(t_b=component.T[t_idx].magnitude,
                                            t_env=env.T[t_idx].magnitude,
                                            h=d['h'],
                                            A=d['area'])
                    assert (Qconv*(component.T[t_idx]-env.T[t_idx])).magnitude >= 0, \
                        '''convection from %s to %s, from low temperature %f to
                    high temperature %f is wrong: %f''' % (
                        component.name, env.name, component.T[t_idx].magnitude,
                        env.T[t_idx].magnitude, Qconv.magnitude)
                to_ret -= Qconv/cap/component.vol.magnitude
            for name, d in component.adv.iteritems():
                Qadv = self.advection(t_out=component.T[t_idx].magnitude*2.0 -
                                      d['t_in'].magnitude,
                                      t_in=d['t_in'].magnitude,
                                      m_flow=d['m_flow'],
                                      cp=d['cp'])
                to_ret -= Qadv/cap/component.vol.magnitude
                assert Qadv >= 0, '''at step %d, %s is heating the system
                by %f watts??? Tin is %f, tout is %f, tcomp is %f''' % (
                    t_idx, component.name, Qadv, d['t_in'].magnitude,
                    (component.T[t_idx]*2 - d['t_in']).magnitude,
                    component.T[t_idx].magnitude)
            return to_ret*units.kelvin/units.seconds

    def BC_center(self, component, t_idx):
        '''Qconduction from the center of a sphere to the first boundary
        (conduction without interface) in watts/meter**3
        :param component: name of the inner most component(mesh element)
        :type component: str
        :param t_idx: timestep at which Qconduction is calculated
        :type t_idx: int
        :return : Qcondction
        :rtype:float, dimensionless
        '''
        conductivity = component.k.magnitude
        T_b = component.T[t_idx].magnitude
        dr = (component.ro - component.ri).magnitude
        return (conductivity*T_b)/(dr**2)

    def convBoundary(self, component, t_b, t_env, h, R):
        '''calculate heat transfer through convective boundray condition
        :param component: name of the outer most solid component
        :type component: str
        :param t_b: temperature of the body
        :type t_b: float
        :param t_env: temperature of the environment(fluid)
        :type t_env: float
        :param h: convective heat transfer coefficient
        :type h: float
        :param R: outer radius of the component
        :type R: float
        :return: dimensionless quantity of Qconv
        :rtype: float
        '''
        r_b = component.ro.magnitude
        k = component.k.magnitude
        dr = component.ri.magnitude-component.ro.magnitude
        T_R = (-h.magnitude/k*t_env + t_b/dr)/(1/dr-h.magnitude/k)
        to_ret = 1/r_b*k*(r_b*t_b-R.magnitude*T_R)/dr**2
        return to_ret

    def heatgenFVM(self, component, power, omegas):
        return (power*component.power_tot.magnitude *
                (1-self.kappa) + sum(omegas))/component.vol.magnitude

    def conductionFVM(self, component, env, t_idx):
        """
        heat transfer by conduction(watts/m3)
        :param component: name of the component
        :type component: str
        :param env: name of the environment
        :type env: str
        :param t_idx: time step that conduction heat is computed
        :type t_idx: int
        :return: Qond, dimemsionless quantity
        :rtype: float
        """
        T_b = component.T[t_idx].magnitude
        T_env = env.T[t_idx].magnitude
        r_b = component.ro.magnitude
        r_env = env.ro.magnitude
        dr = (component.ro-component.ri).magnitude
        k = component.k.magnitude
        return k/r_b * (r_b * T_b - r_env * T_env)/(dr**2)

    def advection(self, t_out, t_in, m_flow, cp):
        ''' calculate heat transfer by advection in watts
        :param t_out: outlet temperature
        :type t_out: float
        :param t_in: inlet temperature
        :type t_in: float
        :param m_flow: mass flow rate though the control volume
        :type m_flow: float
        :param cp: specific heat capacity of the fluid
        :type cp: float
        :return: dimemsionless quantity of Qadvective
        :rtype: float
        '''
        if t_out > t_in:
            return m_flow.magnitude*cp.magnitude*(t_out-t_in)
        else:
            return 0.0

    def convection(self, t_b, t_env, h, A):
        """
        heat transfer by convection(watts)
        :param t_b: The temperature of the body
        :type t_b: float.
        :param t_env: The temperature of the environment
        :type t_env: float.
        :param h: the heat transfer coefficient between environment and body
        :type h: float.
        :param A: the surface area of heat transfer
        :type A: float.
        """
        num = (t_b-t_env)
        denom = (1.0/(h.magnitude*A.magnitude))
        return num/denom
