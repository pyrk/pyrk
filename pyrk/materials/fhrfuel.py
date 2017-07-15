from ur import units
from materials.material import Material
from density_model import DensityModel


class Fhrfuel(Material):
    """This class represents the material properties of the homogenized fuel
    layer in the FHR fuel pebble"""
    def __init__(self, name='fhrfuel'):
        """Initalizes a material based on the fuel kernel in a TRISO particle.
        A material has intensive (as opposed to extensive) material properties.
        :param name: The name of the material (i.e., "fuel" or "cool")
        :type name: str.
        """
        Material.__init__(self,
                          name=name,
                          k=self.thermal_conductivity(),
                          cp=self.specific_heat_capacity(),
                          dm=self.density())

    def thermal_conductivity(self):
        return 17*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        return 1818*units.joule/units.kg/units.kelvin

    def density(self):
        return DensityModel(a=2200.0*units.kg/(units.meter**3),
                            model="constant")
