# Licensed under a 3-clause BSD style license - see LICENSE

from inp import validate_ge

class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self, t0=0, tf=1, dt=1,):
        """This class holds information about a reactor kinetics simulation
        """
        self.t0 = validate_ge(t0, 0)
        self.tf = validate_ge(tf, t0)
        self.dt = validate_ge(dt, 0)

    def timesteps(self):
        return (self.tf-self.t0)/self.dt
