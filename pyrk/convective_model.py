from utilities.ur import units
from materials.material import Material

class ConvectiveModel(object):
    """
    This class implement the Wakao correlation for convective heat transfer
    coefficient
    """

    def __init__(self,
                 mat=Material(),
                 h0=0*units.watt/units.meter**2/units.kelvin,
                 m_flow=0*units.kg/units.second,
                 a_flow=0*units.meter**2,
                 length_scale=0*units.meter,
                 model="constant"):
        """
        Initializes the DensityModel object.

        :param model: The keyword for a model type.
        :type model: string
        """
        self.h0 = h0
        self.k = mat.k
        self.cp = mat.cp
        self.mu = mat.mu
        self.m_flow = m_flow
        self.a_flow = a_flow
        self.length_scale = length_scale

        self.implemented = {'constant': self.constant,
                            'wakao': self.wakao}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Convective heat transfer model type "
            msg += model
            msg += " is not an implemented convective model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)

    def h(self, rho, mu):
        """
        Returns the convective heat transfer coefficient

        :param temp: the temperature
        :type temp: float.
        """
        return self.implemented[self.model](rho, mu)

    def constant(self, rho=0*units.kg/units.meter**3, mu=0):
        """
        Returns a constant density, a.

        :param temp: The temperature of the object
        :type temp: float.
        """
        return self.h0

    def wakao(self, rho, mu):
        """
        Returns a linear dependence on temperature ($ a + b*temp$) .

        :param temp: The temperature of the object
        :type temp: float. units of kelvin
        """
        u = self.m_flow/self.a_flow/rho
        Re = rho * self.length_scale * u / mu
        Pr = self.cp * self.mu / self.k
        Nu = 2 + 1.1 * Pr.magnitude ** (1/3.0)*Re.magnitude**0.6
        ret = Nu *self.k/self.length_scale
        return ret
