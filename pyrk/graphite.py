from ur import units
from th_component import THComponent
from density_model import DensityModel
from timer import Timer


class Graphite(THComponent):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal hydraulics subblock
    """
    def __init__(self, name=None,
                 vol=0.0*units.meter**3,
                 T0=0.0*units.kelvin,
                 alpha_temp=0.0*units.delta_k/units.kelvin,
                 timer=Timer(),
                 heatgen=False,
                 power_tot=0):
        """Initalizes a thermal hydraulic component.
        A thermal-hydraulic component will be treated as one "lump" in the
        lumped capacitance model.

        :param name: The name of the component (i.e., "fuel" or "cool")
        :type name: str.
        :param vol: The volume of the component
        :param T0: The initial temperature of the component
        :type T0: float.
        :param alpha_temp: temperature coefficient of reactivity
        :type alpha_temp: float
        :param timer: The timer instance for the sim
        :type timer: Timer object
        :param heatgen: is this component a heat generator (fuel)
        :type heatgen: bool
        """
        THComponent.__init__(self,
                             name=name,
                             vol=vol,
                             k=self.thermal_conductivity(),
                             cp=self.specific_heat_capacity(),
                             dm=self.density(),
                             T0=T0,
                             alpha_temp=alpha_temp,
                             timer=timer,
                             heatgen=heatgen,
                             power_tot=power_tot)

    def thermal_conductivity(self):
        """Graphite thermal conductivity in [W/m-K]

        For H451 nuclear grade graphite:

        Parallel to forming axis:
            150 W/m-K
        Perpendicular to forming axis:
            135 W/m-K

        Burchell, T.D. 2001. “Nuclear Graphite and Radiation Effects.” In
        Encyclopedia of Materials: Science and Technology (Second Edition),
        edited by K.H. Jürgen Buschow, Robert W. Cahn, Merton C. Flemings,
        Bernhard Ilschner, Edward J. Kramer, Subhash Mahajan, and Patrick
        Veyssière, 6310–19. Oxford: Elsevier.
        http://www.sciencedirect.com/science/article/pii/B0080431526011207.


        Also noted in:
            http://www.osti.gov/scitech/servlets/purl/714896/

        """
        return 0.26*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity for H451 graphite [J/kg/K]
        For H451 Graphite, the specific heat capacity at normal operating
        temperatures for this reactor is approximately 1650 [J/kg/K]

        The temperature dependent model arrived at in Ortensi et al is :

        cp = (0.54212
             - (2.42667E-06)*T
             - (9.02725E+01)*pow(T,-1)
             - (4.34493E+04)*pow(T,-2)
             + (1.59309E+07)*pow(T,-3)
             - (1.43688E+09)*pow(T,-4))*4184


        Ortensi, J., M. A. Pope, G. Strydom, R. S. Sen, M. D. DeHart, H.
        D. Gougar, C. Ellis, et al. 2011. “Prismatic Core Coupled
        Transient Benchmark.” Transactions of the American Nuclear Society
        104: 854.
        """
        return 1650.0*units.joule/(units.kg*units.kelvin)

    def density(self):
        """
        Graphite density for H451 nuclear grade graphite is 1740kg/m^3.

        A constant density model appears sufficiently accurate according to
        most sources - Andreades et al in particular:

        Andreades, C., A.T. Cisneros, J.K. Choi, A.Y.K Chong, David L.
        Krumwiede, Lakshana Huddar, Kathryn D. Huff, et al. 2014. Technical
        Description of the `Mark 1’ Pebble-Bed, Fluoride-Salt-Cooled,
        High-Temperature Reactor Power Plant. Thermal Hydraulics Group
        UCBTH-14-002. FHR Project. Berkeley, CA: University of California,
        Berkeley, Department of Nuclear Engineering.


        Note that in the dissertation by M. Fratoni, this number is reported as
        "1.74 kg/m^3". However, this is a units error. The number intended by
        that document was 1.74 g/cm^3, which corresponds to this model.
        """
        return DensityModel(a=1740.*units.kg/(units.meter**3),
                            model="constant")
