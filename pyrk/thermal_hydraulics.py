import th_params
from ur import units


class ThermalHydraulics(object):
    """This class handles calculations and data related to the
    thermal_hydraulics subblock
    """

    def __init__(self):
        self._params = th_params.THParams()

    def dtempdt(self, component, temps, power, omegas, component_names):
        tfuel = temps[component_names["fuel"]]*units.kelvin
        tcool = temps[component_names["cool"]]*units.kelvin
        tmod = temps[component_names["mod"]]*units.kelvin
        trefl = temps[component_names["refl"]]*units.kelvin
        if component == "fuel":
            return self.dtempfueldt(power, omegas, tfuel, tcool, tmod)
        elif component == "cool":
            return self.dtempcooldt(tfuel, tcool)
        elif component == "mod":
            return self.dtempmoddt(tfuel, tmod)
        elif component == "refl":
            return self.dtemprefldt(tfuel, trefl)
        else:
            raise KeyError("This work only supports fuel, cool, mod, and \
                    refl keys")

    def dtempfueldt(self, power, omegas, tfuel, tcool, tmod):
        # check this, it may not get things quite right...
        rho = self._params.rho("fuel", tfuel)
        cp = self._params.cp("fuel")
        vol = self._params.vol("fuel")
        rm = self._params.r("mod")
        amod = self._params.area(set(["mod", "fuel"]))
        afuel = self._params.area(set(["fuel", "cool"]))
        kf = self._params.k("fuel", tfuel)
        hf = self._params.h("fuel")
        power_tot = self._params._power_tot
        # heat_gen = (power_tot/vol/rho/cp)*((1-self._params._kappa)*power +
        # sum(omegas))
        heat_gen = (power_tot)*(power-sum(omegas))
        cond_mod = self.conduction(tfuel, tmod, rm, kf, amod)
        conv_cool = self.convection(tfuel, tcool, hf, afuel)
        S = heat_gen/(rho*cp*vol)
        Q = (- cond_mod - conv_cool)/(rho*cp*vol)
        to_ret = S+Q
        return to_ret

    def dtempcooldt(self, tfuel, tcool):
        h = self._params._core_height
        tinlet = self._params._t_inlet
        v = self._params._vel_cool
        rho = self._params.rho("cool", tcool)
        cp = self._params.cp("cool")
        res = self._params.res("cool", "fuel")
        conv = (2.0*v/h)*(tcool-tinlet)
        afuel = self._params.area(set(["fuel", "cool"]))  # this is one pebble?
        aflow = self._params.flow_area()  # this is the flow path cross section
        cond = (afuel/aflow)*(tfuel - tcool)/(rho*cp*res)
        return cond - conv

    def dtempmoddt(self, tfuel, tmod):
        rho = self._params.rho("mod", tmod)
        cp = self._params.cp("mod")
        vol = self._params.vol("cool")
        res_m = self._params.res("mod", "fuel")
        f = (tmod-tfuel)/res_m/(rho*cp*vol)
        return f

    def dtemprefldt(self, tcool, trefl):
        rho = self._params.rho("refl", trefl)
        cp = self._params.cp("refl")
        vol = self._params.vol("refl")
        res_m = self._params.res("refl", "cool")
        f = (trefl - tcool)/res_m/(rho*cp*vol)
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
