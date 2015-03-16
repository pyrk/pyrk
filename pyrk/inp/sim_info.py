# Licensed under a 3-clause BSD style license - see LICENSE

from inp import validation


class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self, t0=0, tf=1, dt=1, components={}):
        """This class holds information about a reactor kinetics simulation
        """
        self.t0 = validation.validate_ge("t0", t0.magnitude, 0)
        self.tf = validation.validate_ge("tf", tf.magnitude, t0.magnitude)
        self.dt = validation.validate_ge("dt", dt.magnitude, 0)
        self.components = components

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
