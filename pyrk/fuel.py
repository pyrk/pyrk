from ur import units
from material import Material
from density_model import DensityModel


class Fuel(Material):
    """This class represents a material of the system it has material
    properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal hydraulics subblock
    """
    def __init__(self, name="kernel"):
        """Initalizes a material based on the fuel kernel in a TRISO particle.
        A material has intensive (as opposed to extensive) material properties.

        :param name: The name of the material (i.e., "fuel" or "cool")
        :type name: str.
        :param vol: The volume of the material
        :param T0: The initial temperature of the material
        :type T0: float.
        :param alpha_temp: temperature coefficient of reactivity
        :type alpha_temp: float
        :param timer: The timer instance for the sim
        :type timer: Timer object
        :param heatgen: is this material a heat generator (fuel)
        :type heatgen: bool
        """
        Material.__init__(self,
                          name=name,
                          k=self.thermal_conductivity(),
                          cp=self.specific_heat_capacity(),
                          dm=self.density())

    def thermal_conductivity(self):
        return 15*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        return 1818*units.joule/units.kg/units.kelvin # [J/kg/K]

    def density(self):
        return DensityModel(a=2200.0*units.kg/(units.meter**3),
                            model="constant")
