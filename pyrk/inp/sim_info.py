# Licensed under a 3-clause BSD style license - see LICENSE

from inp import validation
from ur import units


class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self, t0=0, tf=1, dt=1, components={},
                 ne=None, th=None):
        """This class holds information about a reactor kinetics simulation
        """
        self.t0 = validation.validate_ge("t0", t0, 0*units.seconds)
        self.tf = validation.validate_ge("tf", tf, t0)
        self.dt = validation.validate_ge("dt", dt, 0*units.seconds)
        self.components = components
        self.ne = validation.validate_exists("ne", ne)
        self.th = validation.validate_exists("th", th)

    def n_entries(self):
        to_ret = 1 + self.ne._n_pg + self.ne._n_dg + len(self.components)
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
