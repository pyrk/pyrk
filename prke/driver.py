import numpy as np

class Driver(object):
    def __init__(self, alphas, temps, p0, t0, tf, dt):
        """Initializes the simulation"""
        initial_state = State(alphas, temps, t0, dt)
        self._states = {t0, intial_state}
        self._precursor_data = PrecursorData("u235", "thermal")
        n_steps = (tf-t0)/dt + 1
        self._tspan = range(t0, tf, num=n_steps)

    def run(self)
        for t in self._tspan:
            step(t)
        self.plot_all()

    def step(self, t):
        self._states[self._t] = State(self._alphas, self._temps[, self._t, 
            self._dt)

    def plot_all(self):
