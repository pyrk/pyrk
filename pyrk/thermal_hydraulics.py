import th_params
from ur import units


class ThermalHydraulics(object):
    """This class handles calculations and data related to the
    thermal_hydraulics subblock
    """

    def __init__(self, components):
        self._params = th_params.THParams()
        self._components = components

    def dtempdt(self, component, temps, power, omegas, t_idx):
        to_ret = 0
        if component.heatgen:
            to_ret += heatgen(component, power)

        b_idx = self._components.index(component.name)
        for env, area in component.cond.iteritems():
            env_idx = self._components.index(env)
            to_ret += component.res*conduction(t_b = temps[b_idx],
                                 t_env = temps[env_idx],
                                 k = component.k,
                                 L = component.vol/area,
                                 A = area)
        for env, d in component.conv.iteritems():
            env_idx = self._components.index(env)
            to_ret += component.res*convection(t_b = temps[b_idx],
                                 t_env = temps[env_idx],
                                 d['h'],
                                 d['area'])
        component.update_temp(timestep=t_idx, dtempdt=to_ret)
        return to_ret

    def heatgen(self, component, power):
        return (component.power_tot*power)*((1-self._params._kappa) + sum(omegas))

    def dtempfueldt(self, power, omegas, tfuel, tcool, tmod):
        # TODO check this, it may not get things quite right...
        S = heat_gen/(rho*cp*vol)
        # heat_gen = (power_tot)*(power-sum(omegas))
        cond_mod = self.conduction(tfuel, tmod, rm, kf, amod)
        conv_cool = self.convection(tfuel, tcool, hf, afuel)
        Q = (- cond_mod - conv_cool)/(rho*cp*vol)
        to_ret = S+Q
        return to_ret

    def dtempcooldt(self, tfuel, tcool):
        h = self._params._core_height
        tinlet = self._params._t_inlet
        v = self._params._vel_cool
        rho = self._params.rho("cool", tcool)
        cp = self._params.cp("cool")
        res = self._params.res_conv("cool", "fuel")
        conv = (2.0*v/h)*(tcool-tinlet)
        afuel = self._params.area(set(["fuel", "cool"]))  # this is one pebble?
        aflow = self._params.flow_area()  # this is the flow path cross section
        vol = self._params.vol("cool")
        cond = (afuel/aflow)*(tfuel - tcool)/res/(rho*cp*vol)
        return cond - conv

    def dtempmoddt(self, tfuel, tmod):
        rho = self._params.rho("mod", tmod)
        cp = self._params.cp("mod")
        vol = self._params.vol("mod")
        res = self._params.res_cond("mod", "fuel")
        f = (tmod-tfuel)/res/(rho*cp*vol)
        return f

    def dtemprefldt(self, tcool, trefl):
        rho = self._params.rho("refl", trefl)
        cp = self._params.cp("refl")
        vol = self._params.vol("refl")
        res = self._params.res_conv("refl", "cool")
        f = (trefl - tcool)/res/(rho*cp*vol)
        return f

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
