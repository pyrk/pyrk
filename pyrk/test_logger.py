# Licensed under a 3-clause BSD style license - see LICENSE.rst
import numpy as np
from scipy.integrate import ode
import importlib
import sys
import logging
logger = logging.getLogger("test logger")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(filename=sys.argv[2], mode="w")
fh.setLevel(level=logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \n %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


#from scipy.integrate._ode import vode
#class my_vode(vode):
#    #overwrite the original Vode ode solver class to change the default step
#    #mode from 2 to 5
#    def step(self, *args):
#        itask = self.call_args[2]
#        self.rwork[0] = args[4]
#        self.call_args[2] = 5
#        r = self.run(*args)
#        self.call_args[2] = itask
#        return r
#

#from utils.logger import logger
from inp import sim_info
from ur import units
from utils import plotter

from th_component import THSuperComponent

np.set_printoptions(precision=5, threshold=np.inf)

infile = importlib.import_module(sys.argv[1])

si = sim_info.SimInfo(timer=infile.ti,
                      components=infile.components,
                      iso=infile.fission_iso,
                      e=infile.spectrum,
                      n_precursors=infile.n_pg,
                      n_decay=infile.n_dg,
                      kappa=infile.kappa,
                      feedback=infile.feedback,
                      rho_ext=infile.rho_ext,
                      uncertainty_param=infile.uncertainty_param)

def log_results():
    logger.info('\nUncertainty param: \n' + str(si.uncertainty_param))

"""Run it as a script"""
if __name__ == "__main__":
    with open('logo.txt', 'r') as logo:
        logger.critical("\nWelcome to PyRK.\n" +
                        "(c) Kathryn D. Huff\n" +
                        "Your simulation is starting.\n" +
                        "Perhaps it's time for a coffee.\n" +
                        logo.read())
    log_results()
    logger.critical("\nSimulation succeeded.\n")
