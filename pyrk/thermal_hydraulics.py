import th_params


class ThermalHydraulics(object):
    """This class handles calculations and data related to the
    thermal_hydraulics subblock
    """

    def __init__(self, components):
        self._params = th_params.THParams()
        self._components = components

    def dtempdt(self, component, temps, power, omegas, t_idx):
        to_ret = 0
        cap = 1.0/(component.rho*component.cp*component.vol)
        if component.heatgen:
            to_ret += cap*self.heatgen(component, power, omegas)
        b_idx = self._components.index(component.name)
        for env, area in component.cond.iteritems():
            env_idx = self._components.index(env)
            to_ret -= cap*self.conduction(t_b=temps[b_idx],
                                          t_env=temps[env_idx],
                                          k=component.k,
                                          L=component.vol/area,
                                          A=area)
        for env, d in component.conv.iteritems():
            env_idx = self._components.index(env)
            to_ret -= cap*self.convection(t_b=temps[b_idx],
                                          t_env=temps[env_idx],
                                          h=d['h'],
                                          area=d['area'])
        component.update_temp(timestep=t_idx, dtempdt=to_ret)
        return to_ret

    def heatgen(self, component, power, omegas):
        return (component.power_tot*power)*((1-self._params._kappa) +
                                            sum(omegas))

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
