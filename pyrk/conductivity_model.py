from pyrk.utilities.ur import units

class ConductivityModel(object):
    """
    This class handles the temperature dependent thermal conductivity
    with the function k(temp).
    """

    def __init__(self,
                 a=0 * units.watt / units.kelvin / units.meter,
                 b=0 * units.watt / units.kelvin / units.meter / units.kelvin,
                 c=None,
                 d=None,
                 model="constant"):
        """
        Initializes the ConductivityModel object.

        :param model: The keyword for a model type.
        :type model: string
        :param a: first coefficient of the model - the constant term 
        :type a: float.
        :param b: first order the temp coefficient T^1.
        :type b: float
        :param c: second order the temp coefficient T^2.
        :type c: float
        :param d: second order the temp coefficient T^3.
        :type d: float
        :param celcius: first order celcius dependent term
        :type celcius: quantity 
        """
        self.a = a.to(units.watt / units.kelvin / units.meter)
        self.b = b.to(units.watt / units.kelvin / units.meter / units.kelvin)
        self.c = c
        self.d = d


        self.implemented = {'constant': self.constant,
                            'linear': self.linear,
                            'sodium': self.sodium}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Conductivity model type "
            msg += model
            msg += " is not an implemented conductivity model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)
        
    def thermal_conductivity(self, temp=0 * units.kelvin):
        """
        Returns the thermal conductivity based on the temperature.

        :param temp: the temperature
        :type temp: float.
        """
        return self.implemented[self.model](temp)
    
    def constant(self, temp=0 * units.kelvin):
        """
        Returns a constant thermal conductivity, a.

        :param temp: The temperature of the object
        :type temp: float.
        """
        return self.a
    
    def linear(self, temp=0.0 * units.kelvin):
        """
        Returns a linear thermal conductivity, a + b * temp (in celcius).

        :param temp: The temperature of the object
        :type temp: float.
        """
        if temp > (273.15*units.kelvin):
            temp_c = temp - (273.15*units.kelvin)
        else:
            return self.a
        
        ret = self.a + self.b * temp_c
        return ret
    
    def sodium(self, temp=0.0 * units.kelvin):

        """Third order thermal conductivity model for the sodium 
        liquid material
        
        ###k &= 124.67 - 0.11381 \, T #b
        # + 5.5226 \times 10^{-5} \, T^2 #c
        # - 1.1842 \times 10^{-8} \, T^3 #d
        """
        
        T = (temp.to('kelvin')).magnitude
        A = 124.67
        B = -0.11381
        C = 5.5226e-5
        D = -1.1842e-8

        ret = A + B*T+ C*(T**2) + D*(T**3)

        return ret * units.watt / units.meter / units.kelvin