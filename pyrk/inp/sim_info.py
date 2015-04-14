# Licensed under a 3-clause BSD style license - see LICENSE

import timer
import neutronics
import reactivity_insertion as ri
import th_system
from ur import units

class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self, t0=0.0*units.seconds,
                 tf=1.0*units.seconds,
                 dt=1.0*units.seconds,
                 components={},
                 iso="u235", e="thermal", n_precursors=6, n_decay=11,
                 kappa=0.0, rho_ext=None):
        """This class holds information about a reactor kinetics simulation
        """
        self.timer = timer.Timer(t0, tf, dt)
        self.components = components
        self.iso = iso
        self.e = e
        self.n_pg = n_precursors
        self.n_dg = n_decay
        self.rho_ext = self.init_rho_ext(rho_ext)
        self.ne = self.init_ne()
        self.th = th_system.THSystem(kappa=kappa, components=components)

    def init_rho_ext(self, rho_ext):
        if rho_ext is None:
            rho_ext = ri.ReactivityInsertion(self.timer)
        return rho_ext

    def init_ne(self):
        ne = neutronics.Neutronics(iso=self.iso, e=self.e,
                                   n_precursors=self.n_pg,
                                   n_decay=self.n_dg,
                                   timesteps=self.timer.timesteps(),
                                   rho_ext=self.rho_ext)
        return ne

    def n_entries(self):
        to_ret = 1 + self.n_pg + self.n_dg + len(self.components)
        return int(to_ret)

    def add_th_component(self, th_component):
        """Adds a thermal-hydralic component to this simulation.
        It should be fully initialized. A single simulation may have many
        thermal-hydralic components. They are held in a dictionary."""

        if th_component.name in self.components:
            msg = "A component named "
            msg += th_component.name
            msg += " already exists in the simulation."
            raise ValueError(msg)
        else:
            self.components[th_component.name] = th_component
            return th_component
