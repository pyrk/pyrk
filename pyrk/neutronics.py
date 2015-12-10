# Licensed under a 3-clause BSD-style license
import numpy as np
from inp import validation as v

from data import precursors as pr
from data import decay_heat as dh
from reactivity_insertion import ReactivityInsertion
from timer import Timer


class Neutronics(object):

    """This class handles calculations and data related to the
    neutronics subblock
    """

    def __init__(self, iso="u235", e="thermal", n_precursors=6, n_decay=11,
                 n_reflector=0, Lambda_ref=0, ref_rho=[], ref_lambda=[],
                 timer=Timer(),
                 rho_ext=None, feedback=False):
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
        :param n_reflector: number of reflector neutron groups for 'two-point'
        point kinetics, every reflector is considered separatly
        :type n_reflector: int
        :param Lambda_ref: mean prompt neutron lifetime in the core without
        reflector(parameter needed for two-point kinetic model for reflectors)
        :type Lambda_ref: float
        :param ref_rho: reactivity gain introduced by reflectors(data for
        implementing two-point kinetic model for reflectors)
        :type ref_rho: list of float
        :param ref_lambda: sum of mean neutron lifetime in the reflector and
        neutron lifetime after it comes back from the reflector(data for
        implementing two-point kinetic model for reflectors)
        :type ref_lambda: list of float
        :param rho_ext: External reactivity, a function of time
        :type rho_ext: function
        :returns: A Neutronics object that holds neutronics simulation info
        """

        self._iso = v.validate_supported("iso", iso,
                                         ['u235', 'pu239', 'sfr', 'fhr'])
        """_iso (str): Fissioning isotope. 'u235', 'pu239', or 'sfr', "fhr"
        are supported."""

        self._e = v.validate_supported("e", e, ['thermal', 'fast'])
        """_e (str): Energy spectrum 'thermal' or 'fast' are supported."""

        self._npg = v.validate_supported("n_precursors", n_precursors, [6, 0])
        """_npg (int): Number of neutron precursor groups. 6 is supported."""

        self._ndg = v.validate_supported("n_decay", n_decay, [11, 0])
        """_ndg (int): Number of decay heat groups. 11 is supported."""

        self._nref = n_reflector

        self._pd = pr.PrecursorData(iso, e, n_precursors)
        """_pd (PrecursorData): A data.precursors.PrecursorData object"""

        if n_reflector is not 0:
            self._Lambda = Lambda_ref
            self._ref_rho = ref_rho
            self._ref_lambda = ref_lambda
        else:
            self._Lambda = self._pd.Lambda()
            self._ref_rho = []
            self._ref_lambda = []


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

    def dpdt(self, t_idx, components, power, zetas, zeta_refs=[]):
        """Calculates the power term. The first in the neutronics block.

        :param t: the time
        :type t: float.
        :param dt: the timestep
        :type dt: float.
        :param components: the THComponents making up this reactor
        :type components: list of THComponent objects
        :param power: the current reactor power in Watts (timestep t-1 ?)
        :type power: float.
        :param zetas: the current delayed neutron precursor populations, zeta_i
        :type zetas: np.ndarray.
        :param rho_r: sum of the reactivity gain by all the reflectors
        :type rho_r: float
        """
        rho = self.reactivity(t_idx, components)
        beta = self._pd.beta()
        lams = self._pd.lambdas()
        Lambda = self._Lambda
        rho_r = sum(self._ref_rho)
        precursors = 0
        ref_precursors = 0
        for j in range(0, len(lams)):
            assert len(lams) == len(zetas)
            precursors += lams[j]*zetas[j]
        if self._nref is not 0:
            for k in range(0, self._nref):
                assert self._nref == len(zeta_refs), '%d, %d' % (
                    self._nref, len(zeta_refs))
                ref_precursors += self._ref_lambda[k]*zeta_refs[k]
        dp = power*(rho - beta - rho_r)/Lambda + precursors + ref_precursors
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
        Lambda = self._Lambda
        lambda_j = self._pd.lambdas()[j]
        beta_j = self._pd.betas()[j]
        return beta_j*power/Lambda - lambda_j*zeta

    def dzeta_refdt(self, t, power, zeta, j):
        """
        Calculates the change in zeta over time at t for j

        :param t: time
        :type t: float, units of seconds
        :param power: the reactor power at this timestep
        :type power: float, in units of watts
        :param Lambda_c: ...
        :param zeta: $\zeta_j$, the concentration for reflector group j
        :type zeta: float
        :param j: the precursor group index
        :type j: int
        """
        Lambda = self._Lambda
        rho_j = self._ref_rho[j]
        lambda_j = self._ref_lambda[j]
        return rho_j*power/Lambda - lambda_j*zeta

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
        t = self._timer.current_timestep() - 1
        rec = {'t_idx': t,
               'rho_tot': self._rho[t],
               'rho_ext':
               self._rho_ext(t_idx=t).to('delta_k').magnitude
               }
        return rec

    def metadata(self, component):
        timestep = self._timer.current_timestep() - 1
        rec = {'t_idx': timestep,
               'component': component.name,
               'rho': component.temp_reactivity(timestep)}
        return rec
