from ur import units
from th_component import THComponent
from density_model import DensityModel


class Flibe(THComponent):
    """This class represents a component of the system it has material and
    geometric properties essential to thermal modeling and heat transfer in
    support of calculations related to the thermal hydraulics subblock
    """
    def __init__(self, name=None, vol=0, T0=0,
                 alpha_temp=0, timesteps=0, heatgen=False, power_tot=0):
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
        :param timesteps: The number of timesteps in this simulation
        :type timesteps: int
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
                             timesteps=timesteps,
                             heatgen=heatgen,
                             power_tot=power_tot)

    def thermal_conductivity(self):
        """FLiBe thermal conductivity in [W/m-K]
        (based on http://www.psfc.mit.edu/library1/catalog/reports/
        1980/80rr/80rr012/80rr012_full.pdf)
        and found in the Andreades et. al Technical Description (pbfhr design
        report)
        """
        return 1.0*units.watt/(units.meter*units.kelvin)

    def specific_heat_capacity(self):
        """Specific heat capacity
        from www-ferp.ucsd.edu/LIB/PROPS/HTS.shtml
        """
        return 2350.0*units.joule/(units.kg*units.kelvin)

    def density(self):
        """
        FLiBe density as a funciton of T. [kg/m^3]
        based on
        http://aries.ucsd.edu/raffray/publications/FST/TOFE_15_Zaghloul.pdf
        it is valid between the melting point and the critical point
        melting point [K]
        t_m = 732.2
        critical point [K]
        t_c = 4498.8
        """
        return DensityModel(a=2415.6*units.kg/(units.meter**3),
                            b=0.49072*units.kg/(units.meter**3)/units.kelvin,
                            model="linear")
