import scipy as sp

class Neutronics(object):
    """This class handles calculations and data related to the 
    neutronics subblock"""

    def __init__(self):


        self.check_keys(cond, spec_caps)
        self._bodies = cond.keys()
        self._k = cond
        self._cp = spec_caps
        self._data = PrecursorData("u235", "thermal")
            
    def check_keys(self, dict1, dict2):
        diff = set(dict1.keys) - set(dict2.keys)
        if len(diff) != 0:
            raise ValueError("The dictionaries for the two dictionaries do not \
            have the same set of keys. They must refer to the same set of \
            bodies.")

    def rhs(self):
        for b in self._bodies:
            self._temp[key] = rhs(cond[key], spec_caps[key]) 
        
        for key in lhs.keys():
            if key in bodies:
                f = self.find_f(key)
        

    def find_f(self, key):
        try :
            self._f[key]
        except(KeyError) : 
            raise KeyError("There is currently no defined function for the \
            temperature of the body: " + key)
        
        sp.integrate.ode(f).set_integrator('dopri5')
    
    def dpowerdt(t, temps, coeffs, Lambda, power, lams, ksis):
        rho = rho(t, temps, coeffs)
        beta = self._data.beta()
        precursors = 0
        for l in len(lams):
            precursors += lams[l]*ksis[l]
        dp = power*(rho - beta)/Lambda + precursors
        return dp

    def dksi_jdt(Lambda, power, j):
        lam = lams[j]
        ksi = ksi[j] # since this varies, we need last timesteps ksi
        beta = self._data.beta(j)
        return beta*power/Lambda - lam*ksi

    def f(t, y, *f_args):

        for key in bodies:

        return lhs #a scalar, array, or list
