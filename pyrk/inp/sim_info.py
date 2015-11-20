# Licensed under a 3-clause BSD style license - see LICENSE
import numpy as np

from timer import Timer
import neutronics
import reactivity_insertion as ri
import th_system
from db import database


class SimInfo(object):
    """This class holds information about a reactor kinetics simulation"""

    def __init__(self,
                 timer=Timer(),
                 components={},
                 iso="u235",
                 e="thermal",
                 n_precursors=6,
                 n_decay=11,
                 kappa=0.0,
                 rho_ext=None,
                 feedback=False,
                 plotdir='images',
                 infile='input.py',
                 db=None):
        """This class holds information about a reactor kinetics simulation

        :param timer: the Timer object for the simulation
        :type timer: Timer
        :param components: the components making up the reactor
        :type components: dictionary
        :param iso: the main fissioning isotope, decides precursor data
        :type iso: only a few values are supported. see PrecursorData class
        :param e: spectrum ("fast", "thermal", etc.)
        :type e: string
        :param n_precursors: number of delayed precursor groups
        :type n_precursors: int
        :param n_decay: number of decay groups
        :type n_decay: int
        :param kappa: the value for kappa, a decay heat parameter
        :type kappa: float
        :param rho_ext: external reactivity
        :type rho_ext: a ReactivityInsertion object or None
        :param feedback: is reactivity feedback present in the simulation
        :type feedback: bool
        :param plotdir: the directory where the plots will be placed
        :type plotdir: string
        """
        self.timer = timer
        self.components = components
        self.iso = iso
        self.e = e
        self.n_pg = n_precursors
        self.n_dg = n_decay
        self.rho_ext = self.init_rho_ext(rho_ext)
        self.feedback = feedback
        self.ne = self.init_ne()
        self.kappa = kappa
        self.th = th_system.THSystem(kappa=kappa, components=components)
        self.y = np.zeros(shape=(timer.timesteps(), self.n_entries()),
                          dtype=float)
        self.plotdir = plotdir
        self.infile = infile
        if db is not None:
            self.db = db
        else:
            self.db = database.Database()
        self.register_recorders()

    def register_recorders(self):
        self.db.register_recorder('metadata', 'sim_info', self.record,
                                  timeseries=False)
        self.db.register_recorder('metadata', 'sim_input', self.metadata,
                                  timeseries=False)
        self.db.register_recorder('neutronics', 'neutronics_params',
                                  self.ne.record,
                                  timeseries=True)

        for c in self.components:
            self.db.register_recorder('neutronics', 'neutronics_timeseries',
                                      lambda: self.ne.metadata(c),
                                      timeseries=True)
            self.db.register_recorder('th', 'th_timeseries',
                                      c.record,
                                      timeseries=True)
            self.db.register_recorder('th', 'th_params',
                                      c.metadata,
                                      timeseries=False)
        # TODO: for all n_pg and n_dg, report zetas and omegas

    def init_rho_ext(self, rho_ext):
        """Initializes reactivity insertion object for the none case.

        :param rho_ext: external reactivity
        :type rho_ext: a ReactivityInsertion object or None
        """
        if rho_ext is None:
            rho_ext = ri.ReactivityInsertion(self.timer)
        return rho_ext

    def init_ne(self):
        """Initializes the neutronics object owned by the siminfo object
        """
        ne = neutronics.Neutronics(iso=self.iso, e=self.e,
                                   n_precursors=self.n_pg,
                                   n_decay=self.n_dg,
                                   timer=self.timer,
                                   rho_ext=self.rho_ext,
                                   feedback=self.feedback)
        return ne

    def n_components(self):
        """The number of components in the simulation.
        """
        to_ret = len(self.components)
        return to_ret

    def n_entries(self):
        """The number of entries in the pde to be solved
        """
        to_ret = 1 + self.n_pg + self.n_dg + len(self.components)
        return int(to_ret)

    def add_th_component(self, th_component):
        """Adds a thermal-hydralic component to this simulation.
        It should be fully initialized. A single simulation may have many
        thermal-hydralic components. They are held in a dictionary.

        :param th_component: the th_component to add to the system
        :type th_component: THComponent
        """

        if th_component.name in self.components:
            msg = "A component named "
            msg += th_component.name
            msg += " already exists in the simulation."
            raise ValueError(msg)
        else:
            self.components[th_component.name] = th_component
            return th_component

    def get_git_revision_hash(self):
        import subprocess
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'])

    def get_git_revision_short_hash(self):
        import subprocess
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

    def get_timestamp(self):
        # time since epoch, a float
        import time
        ts = time.time()
        # human readable time, a string
        import datetime
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return ts, st

    def get_input_blob(self, filename):
        with open(filename, 'r') as f:
            instring = f.read()
            return instring

    def add_entry(table, rec):
        for k, v in rec.iteritems():
            table.row[k] = v
            table.row.append()
            table.flush()

    def get_sim_hash(self):
        # TODO fix. Currently nonsense
        return 010101010101010101

    def record(self):
        rec = {'t0': self.timer.t0.magnitude,
               'tf': self.timer.tf.magnitude,
               'dt': self.timer.dt.magnitude,
               't_feedback': self.timer.t_feedback.magnitude,
               'iso': self.iso,
               'e': self.e,
               'n_pg': self.n_pg,
               'n_dg': self.n_dg,
               'kappa': self.kappa,
               'plotdir': self.plotdir}
        return rec

    def metadata(self):
        ts, st = self.get_timestamp()
        rec = {'simhash': self.get_sim_hash(),
               'timestamp': ts,
               'humantime': st,
               'revision': self.get_git_revision_short_hash(),
               'inputblob': self.get_input_blob(self.infile)
               }
        return rec
