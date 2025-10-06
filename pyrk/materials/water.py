from pyrk.utilities.ur import units
from pyrk.materials.liquid_material import LiquidMaterial

from pyXSteam.XSteam import XSteam

class WaterDensity():
    def __init__(self, pressure, steam_table):
        """Initializes the WaterDensity object

        :param pressure: Water pressure in MPa
        :type pressure: float.
        :param pressure: XSteam table containing water properties
        :type pressure: pyXSteam.XSteam.XSteam

        """
        self.pressure = pressure
        self.steam_table = steam_table

    def rho(self, temp=0 * units.kelvin):
        """
        Returns the density based on the temperature

        :param temp: the temperature
        :type temp: float.
        """
        if temp.magnitude == 0:
            temp = 900 * units.kelvin
        return self.steam_table.rho_pt(self.pressure, temp.magnitude) * units.kg / pow(units.meter, 3)

class Water(LiquidMaterial):
    """This class represents Water. It inherits from the material
    class and possesses attributes intrinsic to water. Relies on the
    pyxsteam package.

    """

    def __init__(self, name="water", pressure=0.101325):
        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param pressure: Water pressure in MPa
        :type pressure: float.
        """
        self._steam_table = XSteam(XSteam.UNIT_SYSTEM_BARE) # m/kg/sec/K/MPa/W
        self._pressure = pressure
        LiquidMaterial.__init__(self,
                                name=name,
                                k=self.thermal_conductivity(),
                                cp=self.specific_heat_capacity(),
                                dm=self.density())

    def thermal_conductivity(self):
        """Water thermal conductivity in [W/m-K]. Based on the saturated liquid
        thermal conductivity from pyXSteam.
        """
        return self._steam_table.tcL_p(self._pressure) * units.watt / (units.meter * units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity of water [J/kg/K]. Based on the saturated
        liquid heat capacity from pyXSteam.
        """
        return self._steam_table.CpL_p(self._pressure) * units.joule / (units.kg * units.kelvin)

    def density(self):
        """
        Water density as a funciton of T. [kg/m^3]
        """
        return WaterDensity(self._pressure, self._steam_table)
