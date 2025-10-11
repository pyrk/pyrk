from pyrk.materials.material import Material
from pyrk.utilities.ur import units
from pyrk.density_model import DensityModel
from pyrk.inp import validation
from pyrk.conductivity_model import ConductivityModel
from pyrk.viscosity_model import ViscosityModel


class LiquidMaterial(Material):
    ''' subclass of material for liquid'''

    def __init__(self,
                 name=None,
                 k=ConductivityModel(),
                 cp=0 * units.joule / units.kg / units.kelvin,
                 dm=DensityModel(),
                 mu=ViscosityModel()):
        """Initalizes a material

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param km: The thermal conductivity of the component
        :type km: ConductivityModel object
        :param cp: specific heat capacity, :math:`c_p`, in :math:`J/kg-K`
        :type cp: float, pint.unit.Quantity :math:`J/kg-K`
        :param dm: The density of the material
        :type dm: DensityModel object
        :param mu: dynamic viscosity(for fluid), :math:`mu`, in :math:`Pa.s`
        :type mu: ViscosityMode() object
        """

        Material.__init__(self, name, k, cp, dm)

        if isinstance(mu, ViscosityModel):
            self.mu = mu
        else:
            mu = mu.to('pascal*seconds')
            assert mu.units == (units.pascal * units.seconds), \
            "mu must be pascal * seconds"
            self.mu = ViscosityModel(model='constant', 
                                    a=mu)
            
    def dynamic_viscosity(self,temp):
        """
        The dynamic viscosity of this material as a function of temperature.

        :param temp: the temperature
        :type temp: pint quantity in units.kelvin
        :return: the dynamic viscosity of this component
        :rtype: float, in units of :math:`pa /cdot s`
        """
        ret = self.mu.dynamic_viscosity(temp)
        return ret