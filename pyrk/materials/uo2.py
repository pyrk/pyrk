from pyrk.utilities.ur import units
from pyrk.materials.material import Material
from pyrk.density_model import DensityModel


class UO2(Material):
    """This class represents the material properties of UO2 fuel. 

    All of the quantities in this class come from the following reference:
        
    Popov, S. G., V. K. Ivanov, J. J. Carbajo, G. L. Yoder
    2000. ''Thermophysical properties of MOX and UO2 fuels
    including the effects of radiation'' ORNL/TM-2000/351
    https://info.ornl.gov/sites/publications/Files/Pub57523.pdf
    """

    def __init__(self, name='uo2'):
        """Initalizes a material based on UO2 fuel.
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
        """
        UO2 thermal conductivity in [W/m-K]

        Popov et al. present models that account for the effect of radiation
        and temperature on thermal conducticvity (see Table 6.2 in Popov et
        al.). For simplicity, we select the unirradiated material at normal
        operating temperatures (873K)
        """

        return 3.89 * units.watt / (units.meter * units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity for UO2 solid fuel [J/kg/K]
        For UO2, the specific heat capacity at normal operating
        temperatures for this reactor (~900K) is approximately 309.18 [J/kg/K].
        See Table 4.3 in Popov et al.

        The temperature dependent model recommended by Popov et al is :

        .. math::

            c_p &= C_1 \\times \\frac{\\theta}{T}^{2} \\times \\frac{e^{\\frac{\\theta}{T}}}{\\right(e^{\\frac{\\theta}{T}} -1\\left)^2}\\\\
               &+ 2 \\times C_2 \\times T\\\\
               &+ C_3 \\times E_a \\times e^{\\frac{-E_a}{T}} \\times T^{-2}\\\\


        where
        .. math::

            C_1 &= 302.27\\\\
            C_2 &= 8.463 \\times 10^{-3}\\\\
            C_3 &= 8.751 \\times 10^{7}\\\\
            \\theta &= 548.68\\\\
            E_a &= 18531.7\\\\


        """
        return 309.18 * units.joule / units.kg / units.kelvin

    def density(self):
        """
        UO2 density is 10766kg/m^3 at normal reactor operating temperatures.
        See Table 4.2 in Popov et al.

        """

        return DensityModel(a=10766 * units.kg / (units.meter**3),
                            model="constant")
