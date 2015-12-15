import numpy as np
from inp import validation
from utilities.ur import units
import logging
log = logging.getLogger(__name__)


class Timer(object):
    """This class holds information about time"""

    def __init__(self,
                 t0=0.0*units.seconds,
                 tf=1.0*units.seconds,
                 dt=1.0*units.seconds,
                 t_feedback=0.0*units.seconds):
        """Initialize the timer object. There should be only one.

        :param t0: first times in the simulation
        :type t0: float, units of seconds
        :param tf: last time in the simulation
        :type tf: float, units of seconds
        :param dt: size of the timestep
        :type dt: float, units of seconds
        """
        self.t0 = validation.validate_ge("t0", t0, 0.0*units.seconds)
        self.t_feedback = validation.validate_ge("t_feedback", t_feedback, t0)
        self.tf = validation.validate_ge("tf", tf, t_feedback)
        self.dt = validation.validate_g("dt", dt, 0.0*units.seconds)
        self.series = units.Quantity(np.linspace(start=t0.magnitude,
                                                 stop=tf.magnitude,
                                                 num=self.timesteps()),
                                     'seconds')
        self.ts = 0
        self.t_idx_feedback = self.t_idx(t_feedback)

    def t_idx(self, time):
        """given the actual time, in seconds, this returns the index of t.

        :param time: the actual time
        :type time: float, units of seconds
        :return: index
        """
        return self.idx_from_t(time=time, t0=self.t0, dt=self.dt)

    def idx_from_t(self, time, t0, dt):
        """given the any time, in seconds, this returns the index of t.

        :param time: any time to convert
        :type time: float, units of seconds
        :param time: start time for conversion calc
        :type time: float, units of seccnds
        :param time: size of the timestep for the conversion calc
        :type time: float, units of seconds
        :return: index
        """
        num = float(time.magnitude) - float(t0.magnitude)
        denom = float(dt.magnitude)
        return int(round(num/denom))

    def t(self, t_idx):
        """given the index of t, a dimensionless int, this returns the time in
        seconds

        :param t_idx: the index to convert to simulation time
        """
        return self.t0 + self.dt*float(t_idx)

    def timesteps(self):
        """Returns the number of timesteps in this simulation"""
        return self.t_idx(self.tf) + 1

    def advance_one_timestep(self):
        """Advances the timer one timestep"""
        self.advance_time(self.t(self.ts+1))
        return self.ts

    def advance_time(self, time):
        """Advances the timer to a specific time

        :param time: the time to advance to
        :type time: Quantity units seconds
        """
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
