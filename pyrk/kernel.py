from ur import units
from material import Material
from density_model import DensityModel


class Kernel(Material):
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
        """TRISO Kernel thermal conductivity in [W/m-K]

        A first order, constant value approximation was made
        based on Petti, Martin, Phelip, Fig 1.11


        Petti, Martin, Phelip et al
        http://www.sciencedirect.com/science/article/pii/S0022311510003284#bib9

        Note that temperature dependent thermal conductivity model could be
        implemented in the place of this constant model based on Powers and
        Wirth:
        http://www.sciencedirect.com/science/article/pii/S0022311510003284
        """
        return 1.5*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity for TRISO kernel [J/kg/K]

        The value 0.3 J/g/K was extracted from Ortensi et al in Figure 11, page
        12.

        Ortensi, J., and A. M. Ougouag. 2009. "Improved Prediction of the
        Doppler Effect in TRISO Fuel." In Proceedings of International
        Conference on Mathematics, Computational Methods, and Reactor Physics
        (M&C 2009), Saratoga Springs, NY.
        http://www.inl.gov/technicalpublications/Documents/4187480.pdf.

        Note that a temperature dependent model could be implemented based on
        that work.
        """
        ortensi = 0.3*units.joule/(units.g*units.kelvin)  # [J/g/K]
        return ortensi.to('joule/kg/kelvin')  # [J/kg/K]

    def density(self):
        """
        Kernel density for TRISO kernel is 10500.0kg/m^3

        A constant density model appears sufficiently accurate according to
        most sources - Andreades et al in particular:

        Andreades, C., A.T. Cisneros, J.K. Choi, A.Y.K Chong, David L.
        Krumwiede, Lakshana Huddar, Kathryn D. Huff, et al. 2014. Technical
        Description of the 'Mark 1' Pebble-Bed, Fluoride-Salt-Cooled,
        High-Temperature Reactor Power Plant. Thermal Hydraulics Group
        UCBTH-14-002. FHR Project. Berkeley, CA: University of California,
        Berkeley, Department of Nuclear Engineering.

        """
        return DensityModel(a=10500.0*units.kg/(units.meter**3),
                            model="constant")
