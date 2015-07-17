from ur import units
from material import Material
from density_model import DensityModel


class Mod(Material):
    """This class represents graphite materials. It inherits from the material
    class and has attributes intrinsic to graphite.
    """
    def __init__(self, name="graphite"):
        """Initalizes a material

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
        Graphite thermal conductivity in [W/m-K]
        For H451 nuclear grade graphite:

        Parallel to forming axis:
        150 W/m-K
        Perpendicular to forming axis:
        135 W/m-K

        Burchell, T.D. 2001. ''Nuclear Graphite and Radiation Effects.'' In
        Encyclopedia of Materials: Science and Technology (Second Edition),
        edited by K.H. Jurgen Buschow, Robert W. Cahn, Merton C. Flemings,
        Bernhard Ilschner, Edward J. Kramer, Subhash Mahajan, and Patrick
        Veyssiere, 6310-19. Oxford: Elsevier.
        http://www.sciencedirect.com/science/article/pii/B0080431526011207

        Also noted in:
        http://www.osti.gov/scitech/servlets/purl/714896/
        """
        return 15*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity for H451 graphite [J/kg/K]
        For H451 Graphite, the specific heat capacity at normal operating
        temperatures for this reactor is approximately 1650 [J/kg/K]

        The temperature dependent model arrived at in Ortensi et al is :

        .. math::
            cp = (0.54212
                - (2.42667E-06)*T
                - (9.02725E+01)*pow(T,-1)
                - (4.34493E+04)*pow(T,-2)
                + (1.59309E+07)*pow(T,-3)
                - (1.43688E+09)*pow(T,-4))*4184


        Ortensi, J., M. A. Pope, G. Strydom, R. S. Sen, M. D. DeHart, H.
        D. Gougar, C. Ellis, et al. 2011. ''Prismatic Core Coupled
        Transient Benchmark.'' Transactions of the American Nuclear Society
        104: 854.
        """
        return 684*units.joule/(units.kg*units.kelvin)

    def density(self):
        """
        Graphite density for H451 nuclear grade graphite is 1740kg/m^3.

        A constant density model appears sufficiently accurate according to
        most sources - Andreades et al in particular:

        Andreades, C., A.T. Cisneros, J.K. Choi, A.Y.K Chong, David L.
        Krumwiede, Lakshana Huddar, Kathryn D. Huff, et al. 2014. Technical
        Description of the Mark 1 Pebble-Bed, Fluoride-Salt-Cooled,
        High-Temperature Reactor Power Plant. Thermal Hydraulics Group
        UCBTH-14-002. FHR Project. Berkeley, CA: University of California,
        Berkeley, Department of Nuclear Engineering.


        Note that in the dissertation by M. Fratoni, this number is reported as
        "1.74 kg/m^3". However, this is a units error. The number intended by
        that document was 1.74 g/cm^3, which corresponds to this model.
        """
        return DensityModel(a=1740.*units.kg/(units.meter**3),
                            model="constant")
