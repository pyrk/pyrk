import six
from pyrk.th_component import THSuperComponent
from pyrk.utilities.ur import units
from pyrk.materials.liquid_material import LiquidMaterial


class THSystem(object):

    """This class models:

    - lumped capacitance model for slab geometry
    - 1-D heat diffusion in spherical geometry, for heat
      generation at any radius in the sphere,
    - advective heat transfer by fluid
    - convective heat transfer at the solid surface to fluid.
    """

    def __init__(self, kappa, components):
        self.kappa = kappa
        self.components = components

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

    def dtempdt(self, component, power, omegas, t_idx):
        '''compute the derivative dtemperature/dt

        :param component: name of the component that dtemp/dt is calculated
        :type component: str
        :param power: nuclear power density
        :type power: float
        :param omegas: decay heat nuclear data
        :type omegas: list
        :param t_idx: the timestep that dtempdt is calculated for
        :type t_idx: int
        :return: value of dtemp/dt
        :rtype: float, kelvin/s
        '''
        to_ret = 0.0
        if isinstance(component, THSuperComponent):
            #  return 0 for superComponent, doesn't calculate the temperature
            #  variation of superComponent
            return to_ret * units.kelvin / units.second
        else:
            cap = (component.rho(t_idx).magnitude * component.cp.magnitude)
            if component.sph and component.ri.magnitude == 0.0:
                Qcent = self.BC_center(component, t_idx)
                to_ret -= Qcent / cap
            for interface, d in six.iteritems(component.convBC):
                env = self.comp_from_name(interface)
                QconvBC = self.convBoundary(component,
                                            t_b=component.T[t_idx].magnitude,
                                            t_env=env.T[t_idx].magnitude,
                                            h=d["h"].h(env.rho(t_idx),
                                                       env.mat.mu),
                                            R=d["R"])
                to_ret -= QconvBC / cap
            if component.heatgen:
                to_ret += self.heatgen(component, power, omegas) / cap
            for interface, d in six.iteritems(component.cond):
                env = self.comp_from_name(interface)
                if component.sph:
                    Qcond = self.conductionFVM(component, env, t_idx)
                else:
                    Qcond = self.conduction_slab(component, env, t_idx,
                                                 L=d["L"],
                                                 A=d["area"])
                to_ret -= Qcond / cap
            for interface, d in six.iteritems(component.conv):
                env = self.comp_from_name(interface)
                if isinstance(env, THSuperComponent):
                    Tr = env.compute_tr(component.T[t_idx].magnitude,
                                        env.sub_comp[-2].T[t_idx].magnitude,
                                        h=d['h'].h(component.rho(t_idx),
                                                   component.mat.mu).magnitude)
                    Qconv = self.convection(t_b=component.T[t_idx].magnitude,
                                            t_env=Tr,
                                            h=d['h'].h(component.rho(t_idx),
                                                       component.mat.mu),
                                            A=d['area'])
                    assert (Qconv * (component.T[t_idx].magnitude - Tr)) >= 0, '''
                    convection from %s to %s, from low temperature %f to
                    high %f is not physical: %f''' % (
                        component.name, env.name, component.T[t_idx].magnitude,
                        Tr, Qconv.magnitude)
                else:
                    if isinstance(component.mat, LiquidMaterial):
                        h_conv = d['h'].h(component.rho(t_idx),
                                          component.mat.mu)
                    else:
                        if isinstance(env.mat, LiquidMaterial):
                            h_conv = d['h'].h(env.rho(t_idx), env.mat.mu)
                        else:
                            msg = 'neither of the components are liquid:'
                            msg += env.name
                            msg += ' and '
                            msg += component.name
                            raise TypeError(msg)

                    Qconv = self.convection(t_b=component.T[t_idx].magnitude,
                                            t_env=env.T[t_idx].magnitude,
                                            h=h_conv,
                                            A=d['area'])
                    assert (
                        Qconv * (component.T[t_idx] - env.T[t_idx])).magnitude >= 0, \
                        'convection from %s to %s, %fc to %fc is not physical' \
                        % (component.name, env.name,
                           component.T[t_idx].magnitude,
                           env.T[t_idx].magnitude)
                to_ret -= Qconv / cap / component.vol.magnitude
            for name, d in six.iteritems(component.adv):
                Qadv = self.advection(component,
                                      t_idx,
                                      t_in=d['t_in'].magnitude,
                                      m_flow=d['m_flow'],
                                      cp=d['cp'])
                to_ret -= Qadv / cap / component.vol.magnitude
            return to_ret * units.kelvin / units.seconds

    def BC_center(self, component, t_idx):
        '''Volumetric conductive heat flux Qconduction from the center of a
        sphere to the first boundary
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
        return (conductivity * T_b) / (dr**2)

    def convBoundary(self, component, t_b, t_env, h, R):
        '''calculate heat transfer through convective boundray condition
        for the mesh element at the surface of the spherical Supercomponent
        (watts)

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
        dr = component.ri.magnitude - component.ro.magnitude
        T_R = (-h.magnitude / k * t_env + t_b / dr) / \
            (1 / dr - h.magnitude / k)
        to_ret = 1 / r_b * k * (r_b * t_b - R.magnitude * T_R) / dr**2
        return to_ret

    def heatgen(self, component, power, omegas):
        """
        calculate heat transfer by conduction(watts/m3)

        :param component: name of the component
        :type component: str
        :param power: normalized nuclear power generated in the component
        i.e.: power*power_tot = power (in watts)
        :type power: float
        """
        return (power * component.power_tot.magnitude *
                (1 - self.kappa) + sum(omegas)) / component.vol.magnitude

    def conductionFVM(self, component, env, t_idx, L=0.0 * units.meter,
                      k=0.0 * units.meter, A=0.0 * units.meter**2):
        """
        compute volumetric conductive heat transfer by conduction(watts/m3)

        :param component: name of the component
        :type component: str
        :param env: name of the environment
        :type env: str
        :param t_idx: time step that conduction heat is computed
        :type t_idx: int
        :param L: conduction distance
        :type L: float, units meter
        :pram k: conductivity
        :type k: float, units w/mk
        :return: Qond, dimemsionless quantity
        :rtype: float
        """
        T_b = component.T[t_idx].magnitude
        T_env = env.T[t_idx].magnitude
        r_b = component.ro.magnitude
        r_env = env.ro.magnitude
        dr = (component.ro - component.ri).magnitude
        k = component.k.magnitude
        return k / r_b * (r_b * T_b - r_env * T_env) / (dr**2)

    def conduction_slab(self, component, env, t_idx, L,
                        A):
        """
        compute volumetric heat transfer by conduction(watts/m3)

        :param component: name of the component
        :type component: str
        :param env: name of the environment
        :type env: str
        :param t_idx: time step that conduction heat is computed
        :type t_idx: int
        :return: Qond, dimemsionless quantity
        :rtype: float
        """
        assert A.magnitude > 0
        assert L.magnitude > 0
        T_b = component.T[t_idx].magnitude
        T_env = env.T[t_idx].magnitude
        num = (T_b - T_env)
        k = component.k
        denom = (L / (k * A)).magnitude
        return num / denom

    def advection(self, component, t_idx, t_in, m_flow, cp):
        ''' calculate heat transfer by advection in watts

        :param component: name of the component
        :type component: str
        :param t_idx: time step that conduction heat is computed
        :type t_idx: int
        :param t_in: inlet temperature
        :type t_in: float
        :param m_flow: mass flow rate though the control volume
        :type m_flow: float
        :param cp: specific heat capacity of the fluid
        :type cp: float
        :return: dimemsionless quantity of Qadvective
        :rtype: float
        '''

        # check if the temperature is the initial temperature 0degC
        # set Qadv=0 in this case for computation stability
        if component.T[t_idx].to('kelvin') == 0 * units.kelvin:
            Qadv = 0
        else:
            t_out = component.T[t_idx].magnitude * 2.0 - t_in
            Qadv = m_flow.magnitude * cp.magnitude * (t_out - t_in)
        return Qadv

    def mass_trans(self, t_b, t_inlet, H, u):
        """
        :param t_b: The temperature of the body
        :type t_b: float.
        :param t_inlet: The temperature of the flow inlet
        :type t_inlet:
        """
        num = 2.0 * u * (t_b - t_inlet)
        denom = H
        return num / denom

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
        num = (t_b - t_env)
        denom = (1.0 / (h.magnitude * A.magnitude))
        return num / denom

    def custom(self, t_b, t_env, res):
        num = (t_b - t_env)
        denom = res.to(units.kelvin / units.watt)
        return num / denom

    def record(self, component):
        """a recorder function that calls down to each component.
        used for the th/th_timeseries table
        """
        return self.comp_from_name(component).record()

    def metadata(self, component):
        """a recorder function that calls down to each component.
        used for the th/th_params table
        """
        return self.comp_from_name(component).metadata()
