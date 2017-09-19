from pyrk.utilities.ur import units
from pyrk.inp import validation


class ReactivityInsertion(object):
    """This is the default reactivity insertion object class from whence all
    others are derived.

    The default is no external reactivity insertion::

     rho = 0  __________________________________


             t0                                tf
    """

    def __init__(self, timer):
        """
        Creates a reactivity insertion object for driving the transient.

        :param timer: the timer object for the simulation
        :type timer: Timer
        """
        self.timer = timer
        self.vals = [self.f(t_idx) for t_idx in range(timer.timesteps())]

    def f(self, x):
        return 0 * units.delta_k

    def reactivity(self, t_idx):
        return self.vals[t_idx]


class StepReactivityInsertion(ReactivityInsertion):
    """
    Returns a Heaviside step function::


     rho_final               _____________________
                            |
                            |
                            |
                            |
                            |
                            |
     rho_init ______________|

                           t_step
    """

    def __init__(self,
                 timer,
                 t_step=1.0 * units.seconds,
                 rho_init=0.0 * units.delta_k,
                 rho_final=1.0 * units.delta_k):
        """Returns a Heaviside step function as the reactivity insertion object
        for driving the transient.

        :param timer: the timer object for the simulation
        :type timer: Timer
        :param t_step: The time at which the step occurs
        :type t_step: float, seconds
        :param rho_init: Initial reactivity (before t_step)
        :type rho_init: float, units of delta_k
        :param rho_final: Final reactivity (after t_step)
        :type rho_final: float, units of delta_k
        """
        self.rho_init = rho_init.to('delta_k')
        self.rho_final = rho_final.to('delta_k')
        self.t_step = t_step
        ReactivityInsertion.__init__(self, timer=timer)

    def f(self, x):
        if x < self.timer.t_idx(self.t_step):
            return self.rho_init
        else:
            return self.rho_final


class ImpulseReactivityInsertion(ReactivityInsertion):
    """
    Returns an impulse with a width::


     rho_max                 ________________
                            |                |
                            |                |
                            |                |
                            |                |
                            |                |
                            |                |
                            |                |
     rho_init ______________|                |___________

                            t_start         t_end
    """

    def __init__(self,
                 timer,
                 t_start=1.0 * units.seconds,
                 t_end=2.0 * units.seconds,
                 rho_init=0.0 * units.delta_k,
                 rho_max=1.0 * units.delta_k):
        self.t_start = t_start
        self.t_end = t_end
        self.rho_init = rho_init
        self.rho_max = rho_max
        ReactivityInsertion.__init__(self, timer=timer)

    def f(self, x):
        if x < self.timer.t_idx(self.t_start):
            return self.rho_init
        elif x <= self.timer.t_idx(self.t_end):
            return self.rho_max
        else:
            return self.rho_init


class RampReactivityInsertion(ReactivityInsertion):
    """
    Returns a ramp::

     rho_rise
                                   /|
                                  / |
                                 /  |
                                /   |
     rho_final                 /    |__________
                              /
                             /
     rho_init ______________/
                         t_start    t_end
    """

    def __init__(self,
                 timer,
                 t_start=1.0 * units.seconds,
                 t_end=2.0 * units.seconds,
                 rho_init=0.0 * units.delta_k,
                 rho_rise=1.0 * units.delta_k,
                 rho_final=1.0 * units.delta_k):
        self.t_end = validation.validate_g('t_end', t_end, t_start)
        self.t_start = t_start
        self.rho_init = rho_init
        self.rho_rise = rho_rise
        self.rho_final = rho_final
        ReactivityInsertion.__init__(self, timer=timer)

    def f(self, x):
        if x < self.timer.t_idx(self.t_start):
            return self.rho_init
        elif x <= self.timer.t_idx(self.t_end):
            return self.rho_init + \
                self.slope() * (x - self.timer.t_idx(self.t_start))
        else:
            return self.rho_final

    def slope(self):
        rise = self.rho_rise - self.rho_init
        run = self.timer.t_idx(self.t_end) - self.timer.t_idx(self.t_start)
        return rise / run
