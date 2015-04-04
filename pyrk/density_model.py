

class DensityModel(object):
    """
    This class has a public api supporting just one function, rho(temp).
    If the temperature is irrelevant to the model, so be it.
    TODO: It would be great to implement a model that handles dpa.
    """

    def __init__(self, a=0, b=0, model="linear"):
        """
        Initializes the DensityModel object.
        :param model: The keyword for a model type.
        :type model: string
        :param a: first coefficient of the model
        :type a: float.
        :param b: second coefficient of the model.
        :type b: float
        """
        self.a = a
        self.b = b

        self.implemented = {'constant': self.constant,
                            'linear': self.linear}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Density model type "
            msg += model
            msg += " is not an implemented density model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)

    def rho(self, temp=0):
        """
        Returns the density based on the temperature and the irradiation.
        :param temp: the temperature
        :type temp: float.
        """
        return self.implemented[self.model](temp)

    def constant(self, temp=0):
        # yes, we're ignoring the temperature here.
        """
        Returns a .
        :param temp: The temperature of the object
        :type temp: float.
        """
        return self.a

    def linear(self, temp):
        """
        Returns a + b*temp .
        :param temp: The temperature of the object
        :type temp: float.
        """
        ret = self.a + self.b*temp
        return ret
