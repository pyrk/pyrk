from utilities.ur import units
from materials.liquid_material import LiquidMaterial


class ConvectiveModel(object):
    """
    This class defines the model for convective heat transfer coefficient: h
    """

    def __init__(self,
                 h0=0*units.watt/units.meter**2/units.kelvin,
                 mat=LiquidMaterial(),
                 m_flow=None,
                 a_flow=None,
                 length_scale=None,
                 model="constant"):
        """
        Initializes the DensityModel object.

        :param h0: convective heat transfer coefficient when it's a constant
        :type h0: double
        :param mat: material of the fluid
        :type mat: Material object
        :param m_flow: mass flow rate
        :type m_flow: double
        :param a_flow: flow cross section surface area
        :type a_flow: double
        :param length_scale: heat transfer length scale
        :type length_scale: double
        :param model: The keyword for a model type, implemented types are
        'constant' and 'wakao'
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

    def h(self, rho=0*units.kg/units.meter**3, mu=0*units.pascal*units.second):
        """
        Returns the convective heat transfer coefficient

        :param rho: The density of the object
        :type rho: float
        :param mu: The dynamic viscosity of the object
        :type mu: float
        """
        return self.implemented[self.model](rho.to(units.kg/units.meter**3),
                                            mu.to(units.pascal*units.second))

    def constant(self, rho, mu):
        """
        Returns a constant heat transfer coefficient: h0
        :param rho: The density of the object
        :type rho: float
        :param mu: The dynamic viscosity of the object
        :type mu: float

        """
        return self.h0

    def wakao(self, rho, mu):
        """
        This function implements the Wakao correlation for convective heat
        transfer coefficient
        :param rho: The density of the object
        :type rho: float
        :param mu: The dynamic viscosity of the object
        :type mu: float
        """
        u = self.m_flow/self.a_flow/rho
        Re = rho * self.length_scale * u / self.mu
        Pr = self.cp * self.mu / self.k
        Nu = 2 + 1.1 * Pr.magnitude ** (1/3.0)*Re.magnitude**0.6
        ret = Nu * self.k/self.length_scale
        return ret
