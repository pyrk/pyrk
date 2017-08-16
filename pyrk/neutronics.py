# Licensed under a 3-clause BSD-style license
import numpy as np

from pyrk.data import decay_heat as dh
from pyrk.data import precursors as pr
from pyrk.inp import validation as v
from pyrk.reactivity_insertion import ReactivityInsertion
from pyrk.timer import Timer


class Neutronics(object):

    """This class handles calculations and data related to the
    neutronics subblock
    """

    def __init__(self, iso="u235", e="thermal", n_precursors=6, n_decay=11,
                 n_fic=0,
                 timer=Timer(),
                 rho_ext=None,
                 feedback=False):
        """
        Creates a Neutronics object that holds the neutronics simulation
        information.

        :param iso: The fissioning isotope. 'u235' or 'pu239' are supported.
        :type iso: str.
        :param e: The energy spectrum 'thermal' or 'fast' are supported.
        :type e: str.
        :param n_precursors: Number of neutron precursor groups. 6 is supported
        :type n_precursors: int.
        :param n_decay: The number of decay heat groups. 11 is supported.
        :type n_decay: int.
        :param n_fic: number of fictitious neutron groups for 'two-point'
        point kinetics
        :type n_fic: int
        :param rho_ext: External reactivity, a function of time
        :type rho_ext: function
        :returns: A Neutronics object that holds neutronics simulation info
        """

        self._iso = v.validate_supported("iso", iso,
                                         ['u235', 'pu239', 'sfr', 'fhr'])
        """_iso (str): Fissioning isotope. 'u235', 'pu239', or 'sfr', "fhr"
        are supported."""

        self._e = v.validate_supported("e", e, ['thermal', 'fast', 'multipt'])
        """_e (str): Energy spectrum 'thermal' or 'fast' are supported."""

        self._npg = v.validate_supported("n_precursors", n_precursors, [6, 8, 0])
        """_npg (int): Number of neutron precursor groups. 6 is supported."""

        self._ndg = v.validate_supported("n_decay", n_decay, [11, 0])
        """_ndg (int): Number of decay heat groups. 11 is supported."""

        self._nfic = n_fic

        self._pd = pr.PrecursorData(iso, e, n_precursors)
        """_pd (PrecursorData): A data.precursors.PrecursorData object"""

        self._dd = dh.DecayData(iso, e, n_decay)
        """_dd (DecayData): A data.decay_heat.DecayData object"""

        self._timer = timer
        """_timer: the time instance object"""

        self._rho = np.zeros(self._timer.timesteps())
        """_rho (ndarray): An array of reactivity values for each timestep."""

        self._rho_ext = self.init_rho_ext(rho_ext).reactivity
        """_rho_ext (ReactivityInsertion): Reactivity function from the
        reactivity insertion model"""

        self.feedback = feedback
        """feedback (bool): False if no reactivity feedbacks, true otherwise"""

    def init_rho_ext(self, rho_ext):
        if rho_ext is None:
            rho_ext = ReactivityInsertion(self._timer)
        return rho_ext

    def dpdt(self, t_idx, components, power, zetas):
        """Calculates the power term. The first in the neutronics block.

        :param t_idx: the time step index
        :type t_idx: int
        :param components: the THComponents making up this reactor
        :type components: list of THComponent objects
        :param power: the current reactor power in Watts (timestep t-1 ?)
        :type power: float.
        :param zetas: the current delayed neutron precursor populations, zeta_i
        :type zetas: np.ndarray.
        """
        rho = self.reactivity(t_idx, components)
        beta = self._pd.beta()
        lams = self._pd.lambdas()
        Lambda = self._pd.Lambda()
        precursors = 0
        for j in range(0, len(lams)):
            assert len(lams) == len(zetas)
            precursors += lams[j]*zetas[j]
        dp = power*(rho - beta)/Lambda + precursors
        return dp

    def dzetadt(self, t, power, zeta, j):
        """
        Calculates the change in zeta over time at t for j

        :param t: time
        :type t: float, units of seconds
        :param power: the reactor power at this timestep
        :type power: float, in units of watts
        :param zeta: $\zeta_j$, the concentration for precursor group j
        :type zeta: float
        :param j: the precursor group index
        :type j: int
        """
        Lambda = self._pd._Lambda
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

    def reactivity(self, t_idx, components):
        """Returns the reactivity, in $\Delta k$, at time t
        :param t_idx: time step that reactivity is calculated
        :type t_idx: int, index
        :param t_idx_feedback: time step that temperature feedback starts
        :type t_idx_feedback: int, index
        :param components: thermal hydraulic component objects
        :type components: list of THComponent and/or THSuperComponent objects
        """
        rho = {}
        if self.feedback and t_idx > self._timer.t_idx_feedback:
            for component in components:
                rho[component.name] = component.temp_reactivity(t_idx)
        rho["external"] = self._rho_ext(t_idx=t_idx).to('delta_k')
        to_ret = sum(rho.values()).magnitude
        self._rho[t_idx] = to_ret
        return to_ret

    def record(self):
        """A recorder function to hold total and external reactivity
        """
        t = self._timer.current_timestep() - 1
        rec = {'t_idx': t,
               'rho_tot': self._rho[t],
               'rho_ext':
               self._rho_ext(t_idx=t).to('delta_k').magnitude
               }
        return rec

    def metadata(self, component):
        """A recorder function to hold reactivity in each component
        """
        timestep = self._timer.current_timestep() - 1
        rec = {'t_idx': timestep,
               'component': component.name,
               'rho': component.temp_reactivity(timestep)}
        return rec
