# Licensed under a 3-clause BSD style license - see LICENSE
import numpy as np

from timer import Timer
import neutronics
import reactivity_insertion as ri
import th_system


class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self,
                 timer=Timer(),
                 components={},
                 iso="u235",
                 e="thermal",
                 n_precursors=6,
                 n_decay=11,
                 kappa=0.0,
                 rho_ext=None,
                 feedback=False,
                 plotdir='images'):
        """This class holds information about a reactor kinetics simulation

        :param timer: the Timer object for the simulation
        :type timer: Timer
        :param components: the components making up the reactor
        :type components: dictionary
        :param iso: the main fissioning isotope, decides precursor data
        :type iso: only a few values are supported. see PrecursorData class
        :param e: spectrum ("fast", "thermal", etc.)
        :type e: string
        :param n_precursors: number of delayed precursor groups
        :type n_precursors: int
        :param n_decay: number of decay groups
        :type n_decay: int
        :param kappa: the value for kappa, a decay heat parameter
        :type kappa: float
        :param rho_ext: external reactivity
        :type rho_ext: a ReactivityInsertion object or None
        :param feedback: is reactivity feedback present in the simulation
        :type feedback: bool
        :param plotdir: the directory where the plots will be placed
        :type plotdir: string
        """
        self.timer = timer
        self.components = components
        self.iso = iso
        self.e = e
        self.n_pg = n_precursors
        self.n_dg = n_decay
        self.rho_ext = self.init_rho_ext(rho_ext)
        self.feedback = feedback
        self.ne = self.init_ne()
        self.th = th_system.THSystemSphFVM(kappa=kappa, components=components)
        self.y = np.zeros(shape=(timer.timesteps(), self.n_entries()),
                          dtype=float)
        self.plotdir = plotdir

    def init_rho_ext(self, rho_ext):
        """Initializes reactivity insertion object for the none case.

        :param rho_ext: external reactivity
        :type rho_ext: a ReactivityInsertion object or None
        """
        if rho_ext is None:
            rho_ext = ri.ReactivityInsertion(self.timer)
        return rho_ext

    def init_ne(self):
        """Initializes the neutronics object owned by the siminfo object
        """
        ne = neutronics.Neutronics(iso=self.iso, e=self.e,
                                   n_precursors=self.n_pg,
                                   n_decay=self.n_dg,
                                   timer=self.timer,
                                   rho_ext=self.rho_ext,
                                   feedback=self.feedback)
        return ne

    def n_components(self):
        """The number of components in the simulation.
        """
        to_ret = len(self.components)
        return to_ret

    def n_entries(self):
        """The number of entries in the pde to be solved
        """
        to_ret = 1 + self.n_pg + self.n_dg + len(self.components)
        return int(to_ret)

    def add_th_component(self, th_component):
        """Adds a thermal-hydralic component to this simulation.
        It should be fully initialized. A single simulation may have many
        thermal-hydralic components. They are held in a dictionary.

        :param th_component: the th_component to add to the system
        :type th_component: THComponent
        """

        if th_component.name in self.components:
            msg = "A component named "
            msg += th_component.name
            msg += " already exists in the simulation."
            raise ValueError(msg)
        else:
            self.components[th_component.name] = th_component
            return th_component
