from pyrk.utilities.ur import units


class SpecificHeatCapacityModel(object):
    """
    This class has a public api supporting just one function, cp(temp).
    If the temperature is irrelevant to the model, so be it.
    TODO: It would be great to implement a model that handles dpa.
    cp=0 * units.joule / (units.kg * units.kelvin),
    The equation in which models Specific Heat Capacity is y=a+b*T.
    a is the first coefficient of the model and b is the second 
    coefficient of the model.
    """

    def __init__(self,
                 a=0 * units.joule / units.kg,
                 b=0 * units.joule / units.kg / units.kelvin,
                 model="linear"):
        """
        Initializes the SpecificHeatCapactiyModel object.

        :param model: The keyword for a model type.
        :type model: string
        :param a: first coefficient of the model 
        :type a: pint Quantity object with units J/kg/kelvin
        :param b: second coefficient of the model 
        :type b: pint Quantity object with units J/kg/kelvin^2
        """
        self.a = a.to(units.joule / units.kg / units.kelvin)
        self.b = b.to(units.joule / units.kg / pow(units.kelvin,2))

        self.implemented = {'constant': self.constant,
                            'linear': self.linear}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Specific heat capacity model type "
            msg += model
            msg += " is not an implemented specific heat capacity model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)

    def cp(self, temp=0 * units.kelvin):
        """
        Returns the specific heat capacity based on the temperature and the irradiation.

        :param temp: the temperature of the material [kelvin]
        :type temp: pint Quantity object with units of kelvin.
        """
        return self.implemented[self.model](temp)

    def constant(self, temp=0 * units.kelvin):
        """
        Returns a constant specific heat capacity, a.

        :param temp: The temperature of the object
        :type temp: pint Quantity object with units of kelvin.
        """
        return self.a

    def linear(self, temp=0.0 * units.kelvin):
        """
        Returns a linear dependence on temperature ($ a + b*temp$) .

        :param temp: The temperature of the object
        :type temp: pint Quantity object with units of kelvin.
        """
        ret = self.a + self.b * temp
        return ret
