import numpy as np
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
        self.series = units.Quantity(np.linspace(start=t0.magnitude,
                                                 stop=tf.magnitude,
                                                 num=self.timesteps()),
                                     'seconds')
        self.ts = 0

    def t_idx(self, time):
        """given the actual time, in seconds, this returns the index of t."""
        return self.idx_from_t(time=time, t0=self.t0, dt=self.dt)

    def idx_from_t(self, time, t0, dt):
        num = float(time.magnitude) - float(t0.magnitude)
        denom = float(dt.magnitude)
        return int(round(num/denom))

    def t(self, t_idx):
        """given the index of t, a dimensionless int, this returns the time in
        seconds"""
        return self.t0 + self.dt*float(t_idx)

    def timesteps(self):
        return self.t_idx(self.tf) + 1

    def advance_one_timestep(self):
        self.advance_time(self.t(self.ts+1))
        return self.ts

    def advance_time(self, time):
        new_ts = self.t_idx(time)
        old_ts = self.ts
        if (abs(new_ts - old_ts) > 1):
            msg = "At timestep "
            msg += str(self.ts)
            msg += ", which translates to time ("
            msg += str(self.t(self.ts))
            msg += ") the new timestep ("
            msg += str(new_ts)
            msg += ") was more than one step greater than the old timestep: "
            msg += str(old_ts)
            raise RuntimeError(msg)
        self.ts = new_ts
        return validation.validate_le("current time", time, self.tf)

    def current_timestep(self):
        return self.ts

    def current_time(self):
        return self.t(self.ts)
