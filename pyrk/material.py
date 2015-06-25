from inp import validation
from ur import units
from density_model import DensityModel


class Material(object):
    """This class represents a material. Its attributes are material properties
    and behaviors."""

    def __init__(self, name=None,
                 k=0*units.watt/units.meter/units.kelvin,
                 cp=0*units.joule/units.kg/units.kelvin,
                 dm=DensityModel()):
        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param k: The thermal conductivity of the component
        :type k: float.
        :param cp: specific heat capacity, :math:`c_p`, in :math:`J/kg-K`
        :type cp: float, pint.unit.Quantity :math:`J/kg-K`
        :param dm: The density of the material
        :type dm: DensityModel object
        """
        self.name = name
        self.k = k.to('watt/meter/kelvin')
        validation.validate_ge("k", k, 0*units.watt/units.meter/units.kelvin)
        self.cp = cp.to('joule/kg/kelvin')
        validation.validate_ge("cp", cp, 0*units.joule/units.kg/units.kelvin)
        self.dm = dm

    def rho(self, temp):
        """
        The density of this material as a function of temperature.

        :param timestep: the timestep at which to query the temperature
        :type timestep: int
        :return: the density of this component
        :rtype: float, in units of :math:`kg/m^3`
        """
        ret = self.dm.rho(temp)
        return ret
