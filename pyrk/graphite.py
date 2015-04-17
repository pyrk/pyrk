from ur import units
from material import Material
from density_model import DensityModel


class Graphite(Material):
    """This class represents graphite materials. It inherits from the material
    class and has attributes related to graphite.
    """
    def __init__(self, name="graphite"):
        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param k: The thermal conductivity of the component
        :type k: float.
        :param cp: specific heat capacity, $c_p$, in units of $J/kg-K$
        :type cp: float, in units of $J/kg-K$
        :param dm: The density of the component
        :type dm: DensityModel object
        """
        Material.__init__(self,
                          name=name,
                          k=self.thermal_conductivity(),
                          cp=self.specific_heat_capacity(),
                          dm=self.density())

    def thermal_conductivity(self):
        """Graphite thermal conductivity in [W/m-K]
        """
        return 0.26*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity

        """
        return 1650.0*units.joule/(units.kg*units.kelvin)

    def density(self):
        return DensityModel(a=1740.*units.kg/(units.meter**3),
                            model="constant")
