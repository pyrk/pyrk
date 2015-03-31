import logging
logger = logging.getLogger("pyrk logger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename='pyrk.log')
fh.setLevel(level=logging.DEBUG)
logger.addHandler(fh)
