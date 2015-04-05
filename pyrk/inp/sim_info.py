# Licensed under a 3-clause BSD style license - see LICENSE

from inp import validation
from ur import units
import neutronics


class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self, t0=0, tf=1, dt=1, components={},
                 iso="u235", e="thermal", n_precursors=6, n_decay=11,
                 th=None):
        """This class holds information about a reactor kinetics simulation
        """
        self.t0 = validation.validate_ge("t0", t0, 0*units.seconds)
        self.tf = validation.validate_ge("tf", tf, t0)
        self.dt = validation.validate_ge("dt", dt, 0*units.seconds)
        self.components = components
        self.iso = iso
        self.e = e
        self.n_pg = n_precursors
        self.n_dg = n_decay
        self.ne = self.init_ne()
        self.th = validation.validate_not_none("th", th)

    def init_ne(self):
        ne = neutronics.Neutronics(self.iso, self.e, self.n_pg, self.n_dg,
                                   self.timesteps())
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

    def timesteps(self):
        return (self.tf-self.t0)/self.dt + 1
