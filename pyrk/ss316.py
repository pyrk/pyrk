from ur import units
from material import Material
from density_model import DensityModel


class SS316(Material):
    """This class represents a material of the system it has material
    properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal hydraulics subblock
    """
    def __init__(self, name="ss316"):
        """Initalizes a material based on stainless steel 316, a common nuclear
        grade steel.

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
        """SS316 thermal conductivity in [W/m-K]
        from Ragusa, Consistent and Accurate Schemes, 2011
        also from http://www.azom.com/article.aspx?ArticleID=863.

        """
        return 21.5*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity for stainless steel [J/kg/K]
        ASM material data asm.matweb.com

        """
        asm = 500.0*units.joule/(units.kg*units.kelvin)  # [J/kg/K]
        return asm

    def density(self):
        """
        SS316 density in [kg/m^3]
        from asm.matweb.com
        """
        return DensityModel(a=8000.0*units.kg/(units.meter**3),
                            model="constant")
