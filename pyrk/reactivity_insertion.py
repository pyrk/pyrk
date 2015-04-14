from ur import units


class ReactivityInsertion(object):
    """This is the default reactivity insertion object class from whence all
    others are derived."""
    def __init__(self, timer):
        self.timer = timer
        self.vals = [self.f(t_idx) for t_idx in range(timer.timesteps())]

    def f(self, x):
        return 0*units.delta_k

    def reactivity(self, t_idx):
        return self.vals[t_idx]


class StepReactivity(ReactivityInsertion):
    """Returns a Heaviside step function.


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
                 t_step=1.0*units.seconds,
                 rho_init=0.0*units.delta_k,
                 rho_final=1.0*units.delta_k):
        """Returns a Heaviside step function.
        """
        ReactivityInsertion.__init__(self, timer=timer)
        self.rho_init = rho_init
        self.rho_final = rho_final
        self.t_step = t_step

    def f(self, x):
        if x < self.timer.t_idx(self.t_step):
            return self.rho_init
        else:
            return self.rho_final


class ImpulseReactivityInsertion(ReactivityInsertion):
    """
    Returns an impulse with a width


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
                 t_start=1.0*units.seconds,
                 t_end=2.0*units.seconds,
                 rho_init=0.0*units.delta_k,
                 rho_max=1.0*units.delta_k):
        ReactivityInsertion.__init__(self, timer=timer)
        self.t_start = t_start
        self.t_end = t_end
        self.rho_init = rho_init
        self.rho_max = rho_max

    def f(self, x):
        if x < self.timer.t_idx(self.t_start):
            return self.rho_init
        elif x <= self.timer.t_idx(self.t_end):
            return self.rho_max
        else:
            return self.rho_init


class RampReactivityInsertion(ReactivityInsertion):
    """
    Returns a ramp

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
                 t_start=1.0*units.seconds,
                 t_end=2.0*units.seconds,
                 rho_init=0.0*units.delta_k,
                 rho_rise=1.0*units.delta_k,
                 rho_final=1.0*units.delta_k):
        ReactivityInsertion.__init__(self, timer=timer)
        self.t_start = t_start
        self.t_end = t_end
        self.rho_init = rho_init
        self.rho_rise = rho_rise
        self.rho_final = rho_final

    def f(self, x):
        if x < self.timer.t_idx(self.t_start):
            return self.rho_init
        elif x <= self.timer.t_idx(self.t_end):
            return self.slope()*(x - self.timer.t_idx(self.t_start))
        else:
            return self.rho_final

    def slope(self):
        rise = self.rho_rise - self.rho_init
        run = self.timer.t_idx(self.t_end) - self.timer.t_idx(self.t_start)
        return rise/run
