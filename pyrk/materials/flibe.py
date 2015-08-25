from utilities.ur import units
from density_model import DensityModel
from material import Material


class Flibe(Material):
    """This class represents FLiBe. It inherits from the material
    class and possesses attributes intrinsic to flibe.
    All properties from the report: Temperature-Dependent Thermophysical Properties
    for Fluoride Salts and Simulant Fluids
    """
    def __init__(self, name="flibe"):
        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        """
        Material.__init__(self,
                          name=name,
                          k=self.thermal_conductivity(),
                          cp=self.specific_heat_capacity(),
                          dm=self.density())

    def thermal_conductivity(self):
        """FLiBe thermal conductivity in [W/m-K]
        TODO:k= 0.7662+0.0005T (T in celsius)
        """
        return 1.0*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity of flibe [J/kg/K]
        """
        return 2415.78*units.joule/(units.kg*units.kelvin)

    def density(self):
        """
        FLiBe density as a funciton of T. [kg/m^3]

        """
        return DensityModel(a=2413.2172*units.kg/(units.meter**3),
                            b=-0.488*units.kg/(units.meter**3)/units.kelvin,
                            model="linear")
