from utilities.ur import units
from density_model import DensityModel
from materials.material import LiquidMaterial


class Sodium(LiquidMaterial):
    """This class represents Sodium. It inherits from the material
    class and possesses attributes intrinsic to flibe.
    """
    def __init__(self, name="sodium"):
        """Initalizes a material, specifically sodium

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        """
        LiquidMaterial.__init__(self,
                                name=name,
                                k=self.thermal_conductivity(),
                                cp=self.specific_heat_capacity(),
                                dm=self.density())

    def thermal_conductivity(self):
        """Sodium thermal conductivity in [W/m-K]
        TODO, Issue #3

        .. math::

           k &= 124.67 - 0.11381\\times T
             &+ 5.5226 \\times 10^{-5}T^2
             &- 1.1842\\times 10^8T^3

        Below is an estimate of sodium k_th at temperatures around 400C
        based on table 2.1-1 in http://www.ne.anl.gov/eda/ANL-RE-95-2.pdf

        (but, note that wikipedia gives it as 142 W/m-K...)
        """
        return 70.0*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity of Sodium [J/kg/K]
        actually depends on temperature pretty strongly.

        TODO, Issue #4
        The CODATA equation gives the relation:

        .. math ::

           c_p &= 1.6582 - 8.4790\\times10{-4}T
               &+ 4.4541times{-7}T^2 \\\\
               &- 2992.6\\times T^{-2}

        Below is a constant estimate of sodium cp at temperatures around 400C
        based on table 1.1-5 in http://www.ne.anl.gov/eda/ANL-RE-95-2.pdf
        """
        to_ret = 1.3*units.kilojoule/(units.kg*units.kelvin)
        return to_ret.to('J/kg/kelvin')

    def density(self):
        """
        Sodium density as a funciton of T. [kg/m^3]

        The relation is

        .. math::

          \\rho_l &= \\rho_c + f(1-T/T_c) + g(1-T/T_c)^h\\\\
          p_c &= 219 [kg/m^3]\\\\
          f &= 275.32 [-]\\\\
          g &= 511.58 [-]\\\\
          h &= 0.5[-]

        This is based on
        http://www.ne.anl.gov/eda/ANL-RE-95-2.pdf
        It is valid between the melting point and the critical point

        .. math::

           t_m = 371.0K

        .. math::

           t_c = 2503.7K

        """
        return SodiumDensity()


class SodiumDensity(DensityModel):
    def __init__(self):
        """
        Sodium density as a function of T. [kg/m^3]

        The relation is

        .. math::

            \rho_l &= \rho_c + f(1-T/T_c) + g(1-T/T_c)^h\\\\
            p_c &= 219 [kg/m^3]\\\\
            f &= 275.32 [?]\\\\
            g &= 511.58 [?]\\\\
            h &= 0.5

        This is based on
        http://www.ne.anl.gov/eda/ANL-RE-95-2.pdf
        It is valid between the melting point and the critical point

        .. math::

           t_m = 371.0K

        .. math::

           t_c = 2503.7K
        """

        self.rho_c = 219.0*units.kg/pow(units.meter, 3)
        self.T_c = 2503.7*units.kelvin
        self.T_m = 371.0*units.kelvin
        self.f = 275.32*units.kg/pow(units.meter, 3)
        self.g = 511.58*units.kg/pow(units.meter, 3)
        self.h = 0.5

    def hornung(self, temp=0.0*units.kelvin):
        """In the hornung model, K. Hornung [Hornung, 1985] used the available
        data on the sound velocity and the density of Na to determine its
        adiabatic and isothermal compressibility.

        :param temp: the temperature of the sodium
        :type temp: Quantity (units of kelvin)

        """
        to_ret = self.rho_c + self.f*(1 - temp/self.T_c) + \
            self.g*pow((1 - temp/self.T_c), self.h)
        return to_ret.to('kg/m**3')

    def rho(self, temp=0.0*units.kelvin):
        return self.hornung(temp)
