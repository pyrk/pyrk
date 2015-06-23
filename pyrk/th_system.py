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
        for name, d in component.adv.iteritems():
            Qadv = self.advection(t_out=component.T[t_idx]*2.0 - d['t_in'],
                                  t_in=d['t_in'],
                                  m_flow=d['m_flow'],
                                  cp=d['cp'])
            to_ret -= Qadv/cap
            if Qadv.magnitude < 0:
                print '''at step %d, %s is heating the system by %f watts???
            Tin is %f, tout is %f, tcomp is %f''' % (
                t_idx, component.name, Qadv.magnitude, d['t_in'].magnitude,
                (component.T[t_idx]*2 - d['t_in']).magnitude, component.T[t_idx].magnitude)
        for interface, d in component.cond.iteritems():
            env = self.comp_from_name(interface)
            Qcond = self.conduction(t_b=component.T[t_idx],
                                    t_env=env.T[t_idx],
                                    r_b=d['r_b'],
                                    r_env=d['r_env'],
                                    k=d['k'])
            to_ret -= Qcond/cap
            assert (Qcond*(component.T[t_idx]-env.T[t_idx])).magnitude >= 0, 'conduction from %s to %s, from temp %f to %f is wrong %f' % (
                component.name, env.name, component.T[t_idx].magnitude,
                env.T[t_idx].magnitude, Qcond.magnitude)
        for interface, d in component.conv.iteritems():
            env = self.comp_from_name(interface)
            Qconv = self.convection(t_b=component.T[t_idx],
                                    t_env=env.T[t_idx],
                                    h=d['h'],
                                    A=d['area'])
            to_ret -= Qconv/cap
            assert (Qconv*(component.T[t_idx]-env.T[t_idx])).magnitude >= 0, 'cnvection from %s to %s, from temp %f to %f is wrong %f' % (
                component.name, env.name, component.T[t_idx].magnitude,
                env.T[t_idx].magnitude, Qconv.magnitude)
        return to_ret

    def heatgen(self, component, power, omegas):
        '''to do: change this return to include decay heat'''
        return power*component.power_tot

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

    def advection(self, t_out, t_in, m_flow, cp):
        ''' calculate heat transfer by advection in watts
        '''
        if t_out > t_in:
            return m_flow*cp*(t_out-t_in)
        else:
            return 0*units.watts
