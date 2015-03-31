import logging
logger = logging.getLogger("pyrk logger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filename='pyrk.log', mode="w")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - \
                              %(message)s')
fh.setFormatter(formatter)
fh.setLevel(level=logging.DEBUG)
logger.addHandler(fh)
