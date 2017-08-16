from pyrk.density_model import DensityModel
from pyrk.materials.material import Material
from pyrk.utilities.ur import units


class SFRMetal(Material):
    """This class represents SFR Metal fuel. It inherits from the material
    class and possesses attributes intrinsic to SFR metal fuel, as reported in
    T. Sofu, A review of inherent safety characteristics of metal alloy
    sfrmetal-cooled fast reactor fuel against postulated accidents

    http://www.sciencedirect.com/science/article/pii/S1738573315000753
    """
    def __init__(self, name="sfrmetal"):
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
        """SFRMetal thermal conductivity in [W/m-K]
        """
        to_ret = 0.16*units.watt/(units.centimeter*units.kelvin)
        return to_ret.to('watt/meter/kelvin')

    def specific_heat_capacity(self):
        """Specific heat capacity of SFRMetal [J/kg/K]
        actually depends on temperature pretty strongly.

        TODO, Issue #4
        The CODATA equation gives the relation:

        .. math ::

          c_p &= 1.6582 - 8.4790\\times10^{-4}T\\\\
              &+ 4.4541\\times10^{-7}T^2 - 2992.6T^{-2}

        Below is a constant estimate of sfrmetal cp at temperatures around 400C
        based on table 1.1-5 in http://www.ne.anl.gov/eda/ANL-RE-95-2.pdf
        """
        to_ret = 0.17*units.joule/(units.g*units.kelvin)
        return to_ret.to('J/kg/kelvin')

    def density(self):
        """
        SFRMetal density as a funciton of T. [kg/m^3]

        """
        return DensityModel(a=14.1*units.gram/units.cm**3, model='constant')
