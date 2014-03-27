import numpy as np
import matplotlib as mpl

alphas = {
        "fuel": -3.8, 
        "cool": -1.8, 
        "gmod": -0.7, 
        "refl": 1.8
        }
temps = {
        "fuel": 730., 
        "cool": 650., 
        "gmod": 700., 
        "refl": 650.  
        }

class Driver(object):
    def __init__(self, alphas, temps, p0, t0, tf, dt):
        """Initializes the simulation"""
        initial_state = State(self._alphas, temps, t0, dt)
        self._states = {t0, intial_state}
        self._precursor_data = PrecursorData("u235", "thermal")
        n_steps = (tf-t0)/dt + 1
        self._tspan = range(t0, tf, num=n_steps)

    def run(self)
        for t in self._tspan:
            step(t)
        self.plot_all()

    def step(self, t):
        # Should do this in two separate steps:
        # neutronics then thermal hydraulics 
        self._states[t] = State(self._alphas, self._temps[t-self._dt], t, 
            self._dt)
        self._temps[t] = self._states[t]._temps
        self._reactivities[t] = self._states[t]._rho 
        self._powers[t] = self._states[t]._power

    def plot_all(self):
        self._plotter.plot_temps()
        self._plotter.plot_reactivities()
        self._plotter.plot_power()


