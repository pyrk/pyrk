
class ThermalHydraulics(object):
    """This class handles calculations and data related to the 
    thermal_hydraulics subblock"""

    def __init__(self,
            cond,
            spec_caps):
        self.check_keys(cond, spec_caps)
        self._bodies = cond.keys()
        self._k = cond
        self._cp = spec_caps
            
    def check_keys(self, dict1, dict2):
        diff = set(dict1.keys) - set(dict2.keys)
        if len(diff) != 0:
            raise ValueError("The dictionaries of specific heat capacity and 
            conductivity have different keys. They must refer to the same set of 
            bodies")


    def rhs(self):
        for b in self._bodies:
            self._temp[key] = rhs(cond[key], spec_caps[key])


