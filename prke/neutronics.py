import scipy as sp
import precursor_data 

class Neutronics(object):
    """This class handles calculations and data related to the 
    neutronics subblock"""

    def __init__(self):
        self._data = precursor_data.PrecursorData("u235", "thermal")
            
    def check_keys(self, dict1, dict2):
        diff = set(dict1.keys) - set(dict2.keys)
        if len(diff) != 0:
            raise ValueError("The dictionaries for the two dictionaries do not \
            have the same set of keys. They must refer to the same set of \
            bodies.")

    def dpdt(self, t, temps, coeffs, Lambda, power, lams, ksis):
        rho = rho(t, temps, coeffs)
        beta = self._data.beta()
        precursors = 0
        for l in len(lams):
            precursors += lams[l]*ksis[l]
        dp = power*(rho - beta)/Lambda + precursors
        return dp

    def dksidt(self, t, Lambda, power, j):
        lam = lams[j]
        ksi = ksi[j] # since this varies, we need last timesteps ksi
        beta = self._data.beta(j)
        return beta*power/Lambda - lam*ksi

    def dwdt(self, k):
        self._data.w(k)

