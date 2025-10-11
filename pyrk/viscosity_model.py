from pyrk.utilities.ur import units
from numpy import exp,log

class ViscosityModel(object):
    """
    This class handles the temperature dependent
    dynamic viscosity with the function mu(temp).
    """

    def __init__(self,
                 a=0 * units.pascal * units.second,
                 b=0 * units.kelvin,
                 c=0,
                 model="constant"):
        """
        Initializes the ViscosityModel object.

        :param model: The keyword for a model type.
        :type model: string
        :param a: first coefficient of the model
        :type a: float.
        :param b: second coefficient of the model.
        :type b: float
        """
        self.a = a.to(units.pascal * units.second)
        self.b = b.to(units.kelvin)
        self.c = c

        self.implemented = {'constant': self.constant,
                            'exponential': self.exponential,
                            'sodium':self.sodium}

        if model in self.implemented.keys():
            self.model = model
        else:
            self.model = NotImplemented
            msg = "Viscosity model type "
            msg += model
            msg += " is not an implemented viscosity model. Options are:"
            for m in self.implemented.keys():
                msg += m
            raise ValueError(msg)
        
    def dynamic_viscosity(self, temp=0 * units.kelvin):
        """
        Returns the dynamic viscosity based on the temperature.

        :param temp: the temperature
        :type temp: float.
        """
        return self.implemented[self.model](temp)
    
    def constant(self, temp=0 * units.kelvin):
        """
        Returns a constant dynamic viscosity, a.

        :param temp: The temperature of the object
        :type temp: float.
        """
        return self.a
    
    def exponential(self, temp=0.0 * units.kelvin):
        """
        Returns dynamic viscosity using an exponential 
        function in the form
        
        a * exp(b / temp)

        :param temp: The temperature of the object
        :type temp: float.
        """
        if temp.magnitude <= 0:
            raise ZeroDivisionError("Temperature must be greater than zero for viscosity's exponential mode.")

        temp = temp.to(units.kelvin)
        ret = self.a * exp(self.b / temp)
        return ret
    
    def sodium(self, temp=0.0 * units.kelvin):
        """
        Returns dynamic viscosity using an exponential function
        in the form

        a*T^(c) * exp(b/T) 
        
        to conform to http://www.ne.anl.gov/eda/ANL-RE-95-2.pdf
        page 207's model of viscosity

                ln(mu) = -6.4406 -0.3958 ln(T) + 556.835 / T

        :param temp: temperature of object
        :temp type: float 
        """

        T = temp.to(units.kelvin).magnitude
        ret = exp(-6.4406) * T**(- 0.3958) * exp(556.835/T)
        return  ret * units.pascal * units.second