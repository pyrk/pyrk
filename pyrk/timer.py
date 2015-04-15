import math
from inp import validation
from ur import units
import logging
log = logging.getLogger(__name__)


class Timer(object):
    """This class holds information about time"""

    def __init__(self, t0=0.0*units.seconds, tf=1.0*units.seconds,
                 dt=1.0*units.seconds):
        self.t0 = validation.validate_ge("t0", t0, 0*units.seconds)
        self.tf = validation.validate_ge("tf", tf, t0)
        self.dt = validation.validate_ge("dt", dt, 0*units.seconds)
        self.ts = 0
        self.current_t = self.t0

    def t_idx(self, t):
        """given the actual time, in seconds, this returns the index of t."""
        return int(math.floor((t-self.t0)/self.dt))

    def t(self, t_idx):
        """given the index of t, a dimensionless int, this returns the time in
        seconds"""
        return self.t0 + self.dt*t_idx

    def timesteps(self):
        return int((self.tf-self.t0)/self.dt + 1)

    def advance_timestep(self):
        self.ts += 1
        return validation.validate_le("current time", self.t(self.ts), self.tf)

    def current_timestep(self):
        return self.ts

    def current_time(self):
        return self.t(self.ts)
