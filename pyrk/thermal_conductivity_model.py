from pyrk.utilities.ur import units


class ThermalConductivityModel(object):
    """
    This class has a public api supporting just one function, k(temp).
    If the temperature is irrelevant to the model, so be it.
    TODO: It would be great to implement a model that handles dpa.
    """

    def __init__(self,
                 a=0 * units.watt / units.meter,
                 b=0 * units.watt / units.meter / pow(units.kelvin,2),
                 model="linear"):
        """
        Initializes the Thermal Conductivty object.

        :param model: The keyword for a model type.
        :type model: string
        :param a: first coefficient of the model
        :type a: pint Quantity object with units W/m/kelvin
        :param b: second coefficient of the model.
        :type b: pint Quantity object with units W/m/kelvin^2
        """
        self.a = a.to(units.watt / units.meter / units.kelvin)
        self.b = b.to(units.watt / units.meter / pow(units.kelvin, 2))

        self.implemented = {'constant': self.constant,
                            'linear': self.linear}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Thermal Conductivity model type "
            msg += model
            msg += " is not an implemented density model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)

    def k(self, temp=0 * units.kelvin):
        """
        Returns the thermal conductivty based on the temperature and the irradiation.

        :param temp: the temperature
        :type temp: pint Quantity object with units kelvin.
        """
        return self.implemented[self.model](temp)

    def constant(self, temp=0 * units.kelvin):
        """
        Returns a constant thermal conductivity, a.

        :param temp: The temperature of the object
        :type temp: pint Quantity object with units kelvin
        """
        return self.a

    def linear(self, temp=0.0 * units.kelvin):
        """
        Returns a linear dependence on temperature ($ a + b*temp$) .

        :param temp: The temperature of the object
        :type temp: pint Quantity object with units of kelvin
        """
        ret = self.a + self.b * temp
        return ret
