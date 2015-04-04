# Licensed under a 3-clause BSD-style license
import numpy as np


from data import precursors as pr
from data import decay_heat as dh

from ur import units


class Neutronics(object):
    """This class handles calculations and data related to the
    neutronics subblock
    """

    def __init__(self, iso="u235", e="thermal", n_precursors=6, n_decay=11,
                 n_steps=0):
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

        self._n_steps = n_steps
        """_n_steps: number of timesteps in the simulation."""

        self._rho = np.zeros(n_steps)
        """_rho (ndarray): An array of reactivity values for each timestep."""

    def rho_ext(self, t):
        """
        :param t: time
        :type t: float.
        """
        if t >= 0.1*units.seconds and t <= 0.2*units.seconds:
            return 0.0001*units.delta_k
        elif t >= 0.0*units.seconds:
            return 0*units.delta_k
        elif t < 0*units.seconds:
            raise ValueError("Negative times should not happen. Please check \
                    input")
        else:
            return 0

    def dpdt(self, t, dt, components, power, zetas):
        """Calculates the power term. The first in the neutronics block.
        :param t: the time
        :type t: float.
        :param dt: the timestep
        :type dt: float.
        :param coeffs: the temperature coefficients of reactivity for each
        component
        :type coeffs: dict.
        :param power: the current reactor power in Watts (timestep t-1 ?)
        :type power: float.
        :param zetas: the current delayed neutron precursor populations, zeta_i
        :type zetas: np.ndarray.
        """
        rho = self.reactivity(t, dt, components)
        beta = self._pd.beta()
        lams = self._pd.lambdas()
        Lambda = self._pd.Lambda()
        precursors = 0
        for j in range(0, len(lams)):
            precursors += lams[j]*zetas[j]
        dp = power*(rho - beta)/Lambda + precursors
        return dp

    def dzetadt(self, t, power, zeta, j):
        """
        :param t: time
        :type t: float, units of seconds
        :param power: the reactor power at this timestep
        :type power: float, in units of watts
        :param zeta: $\zeta_j$, the concentration for precursor group j
        :type zeta: float #TODO units?
        :param j: the precursor group index
        :type j: int
        """
        Lambda = self._pd.Lambda()
        lambda_j = self._pd.lambdas()[j]
        beta_j = self._pd.betas()[j]
        return beta_j*power/Lambda - lambda_j*zeta

    def dwdt(self, power, omega, k):
        """Returns the change in decay heat for $\omega_k$ at a certain power
        :param power: the reactor power at this timestep
        :type power: float, in units of watts
        :param omega: $\omega_k$ for fission product decay heat group k
        :type omega: float, in units of watts #TODO check
        :param k: the fission product decay heat group index
        :type k: int
        """
        kappa = self._dd.kappas()[k]
        p = power
        lam = self._dd.lambdas()[k]
        return kappa*p-lam*omega

    def reactivity(self, t, dt, components):
        """Returns the reactivity, (units? TODO), at time t
        :param t: time
        :type t: float, units of seconds
        :param dt: timestep size, units of seconds
        :type dt: float, units of seconds
        :param components: thermal hydraulic component objects
        :type components: list of THComponent objects
        """
        rho = {}
        t_idx = int(t/dt)
        for component in components:
            rho[component.name] = component.temp_reactivity(t, dt)
        rho["external"] = self.rho_ext(t).to('delta_k')
        to_ret = sum(rho.values()).magnitude
        self._rho[t_idx] = to_ret
        return to_ret
