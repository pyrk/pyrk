import logging

pyrklog = logging.getLogger("pyrklog")


def set_up_pyrklog(logfile):
    pyrklog.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(filename='pyrk.log', mode="w")
    fh.setLevel(level=logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \n %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the pyrklog
    pyrklog.addHandler(fh)
    pyrklog.addHandler(ch)
