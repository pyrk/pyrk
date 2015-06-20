from ur import units
import math

class THSystem(object):
    """This class handles calculations and data related to the
    thermal hydraulics subblock
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

    def dtempdt(self):
        pass


class THSystemSphPS(THSystem):

    def __init__(self, kappa, components):
        THSystem.__init__(self, kappa, components)

    def dtempdt(self, component, power, omegas, t_idx):
        to_ret = 0*units.kelvin/units.second
        cap = (component.rho(t_idx)*component.cp*component.vol)
        if component.heatgen:
            to_ret += self.heatgen(component, power, omegas)/cap
        if component.adv:
            to_ret += component.advheat
        for interface, d in component.cond.iteritems():
            env = self.comp_from_name(interface)
            to_ret -= self.conduction(t_b=component.T[t_idx],
                                      t_env=env.T[t_idx],
                                      r_b=d['r_b'],
                                      r_env=d['r_env'],
                                      k=d['k'])/cap
        for interface, d in component.conv.iteritems():
            env = self.comp_from_name(interface)
            to_ret -= self.convection(t_b=component.T[t_idx],
                                      t_env=env.T[t_idx],
                                      h=d['h'],
                                      A=d['area'])/cap
        return to_ret
    def heatgen(self, component, power, omegas):
        return (component.power_tot)*((1-self.kappa)*power +
                                      sum(omegas))

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
        denom = (1.0/(h*A))
        return num/denom

    def conduction(self, t_b, t_env, r_b, r_env, k):
        """
        heat transfer by conduction(watts)
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
        num = 4*math.pi*k*(t_b-t_env)
        denom = (1/r_b - 1/r_env)
        return num/denom


