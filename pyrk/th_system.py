from ur import units


class THSystem(object):
    """This class handles calculations and data related to the
    thermal hydraulics subblock
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
