import scipy as sp
import precursor_data 
import decay_data 

component_names = {"fuel":0, "cool":1, "mod":2, "refl":3}

class Neutronics(object):
    """This class handles calculations and data related to the 
    neutronics subblock"""

    def __init__(self, iso, e, n_precursors, n_decay):
        # TODO Add a check that iso is something like "u235" and e is "thermal" 
        # or "fast"
        self._data = precursor_data.PrecursorData(iso, e, n_precursors)
        self._data = decay_data.DecayData(iso, e, n_decay)
        self._rho = {0:0}

    def rho_ext(self, t):
        if t>0 and t<0.1:
            return 1.0
        elif t<0 :
            raise ValueError("Negative times should not happen. Please check \
                    input") 
        else :
            return 0

    def check_keys(self, dict1, dict2):
        diff = set(dict1.keys) - set(dict2.keys)
        if len(diff) != 0:
            raise ValueError("The two dictionaries do not \
            have the same set of keys. They must refer to the same set of \
            bodies.")

    def dpdt(self, t, dt, temps, coeffs, power, zetas):
        rho = self.reactivity(t, dt, temps, coeffs)
        beta = self._data.beta()
        lams = self._data._lambdas
        Lambda = self._data.Lambda()
        precursors = 0
        for l in range(0,len(lams)):
            precursors += lams[l]*zetas[l]
        dp = power*(rho - beta)/Lambda + precursors
        return dp

    def dzetadt(self, t, power, zeta, j):
        Lambda = self._data.Lambda()
        lam = self._data._lambdas[j]
        beta = self._data._betas[j]
        return beta*power/Lambda - lam*zeta

    def dwdt(self, power, k):
        #k = self._data._kappas[k] #TODO
        w = self._data._omegas[k]
        p = power
        #lam = self._data_lambdas_fp[k] #TODO
        k = 0 
        lam = 0
        return k*p-lam*w

    def reactivity(self, t, dt, temps, coeffs):
        drho = {}
        dtemp = {}
        t_idx = int(t/dt)
        for key, alpha in coeffs.iteritems():
            idx = component_names[key]
            dtemp[key] = (temps[t_idx][idx] - temps[0][idx])
            drho[key] = coeffs[key]*dtemp[key]
        drho["external"] = self.rho_ext(t)
        to_ret = sum(drho.values())
        self._rho[t_idx] = to_ret
        return to_ret
