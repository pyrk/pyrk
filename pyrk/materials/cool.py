from ur import units
from density_model import DensityModel
from material import Material
import random

class Cool(Material):
    """This class represents FLiBe. It inherits from the material
    class and possesses attributes intrinsic to flibe.
    """
    def __init__(self, name="flibe", cp=2415.78*units.joule/(units.kg*units.kelvin)):

        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        """
        Material.__init__(self,
                          name=name,
                          k=self.thermal_conductivity(),
                          cp=cp,
                          dm=self.density())

    def thermal_conductivity(self):
        '''TODO 0.7662 + 0.0005*Tc'''
        return 1.0*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity of flibe [J/kg/K]

        from www-ferp.ucsd.edu/LIB/PROPS/HTS.shtml
        """
        return 2415.78*units.joule/(units.kg*units.kelvin)

    def density(self):
        """
        FLiBe density as a funciton of T. [kg/m^3]

        The relation is
        .. math::
        2415 -  0.49072T\]

        This is based on
        http://aries.ucsd.edu/raffray/publications/FST/TOFE_15_Zaghloul.pdf
        it is valid between the melting point and the critical point

        .. math::
        t_m = 732.2

        .. math::
        t_c = 4498.8
        """
        rho = DensityModel(a=2415.6*units.kg/(units.meter**3),
                            b=-0.49072*units.kg/(units.meter**3)/units.kelvin,
                            model="linear")
        return rho
