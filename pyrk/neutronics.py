from data import precursors as pr
from data import decay_heat as dh


component_names = {"fuel": 0, "cool": 1, "mod": 2, "refl": 3}


class Neutronics(object):
    """This class handles calculations and data related to the
    neutronics subblock
    """

    def __init__(self, iso, e, n_precursors, n_decay):
        """
        Creates a Neutronics object that holds the neutronics simulation
        information.


        :param iso: The fissioning isotope. 'u235' or 'pu239' are supported.
        :type iso: str.
        :param e: The energy spectrum 'thermal' or 'fast' are supported.
        :type e: str.
        :param n_precursors: Number of neutron precursor groups. 6 is supported.
        :type n_precursors: int.
        :param n_decay: The number of decay heat groups. 11 is supported.
        :type n_decay: int.
        :returns: A Neutronics object that holds neutronics simulation info
        """

        self._iso = iso
        """_iso (str): Fissioning isotope. 'u235' or 'pu239' are supported."""

        self._e = e
        """_e (str): Energy spectrum 'thermal' or 'fast' are supported."""

        self._npg = n_precursors
        """_npg (int): Number of neutron precursor groups. 6 is supported."""

        self._ndg = n_decay
        """_ndg (int): Number of decay heat groups. 11 is supported."""

        self._pd = pr.PrecursorData(iso, e, n_precursors)
        """_pd (PrecursorData): A data.precursors.PrecursorData object"""

        self._dd = dh.DecayData(iso, e, n_decay)
        """_dd (DecayData): A data.decay_heat.DecayData object"""

        self._rho = {0: 0}
        """_rho (dict): A dictionary of times and reactivity values"""

    def rho_ext(self, t):
        if t > 0 and t < 0.1:
            return 1.0
        elif t < 0:
            raise ValueError("Negative times should not happen. Please check \
                    input")
        else:
            return 0

    def check_keys(self, dict1, dict2):
        diff = set(dict1.keys) - set(dict2.keys)
        if len(diff) != 0:
            raise ValueError("The two dictionaries do not \
            have the same set of keys. They must refer to the same set of \
            bodies.")

    def dpdt(self, t, dt, temps, coeffs, power, zetas):
        rho = self.reactivity(t, dt, temps, coeffs)
        beta = self._pd.beta()
        lams = self._pd.lambdas()
        Lambda = self._pd.Lambda()
        precursors = 0
        for l in range(0, len(lams)):
            precursors += lams[l]*zetas[l]
        dp = power*(rho - beta)/Lambda + precursors
        return dp

    def dzetadt(self, t, power, zeta, j):
        Lambda = self._pd.Lambda()
        lam = self._pd.lambdas()[j]
        beta = self._pd.betas()[j]
        return beta*power/Lambda - lam*zeta

    def dwdt(self, power, omega, k):
        kappa = self._dd.kappas()[k]
        p = power
        lam = self._dd.lambdas()[k]
        return kappa*p-lam*omega

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
