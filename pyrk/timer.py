
import logging


def run_sim(self, si, db, driver):

    logging.info(si.print_str())
    logging.info("Simulation starting.")

    for time in range(si.t0, si.tf, si.dt):
        logging.info("Current time = "+str(time))
        driver.tick()
        driver.tock()
        db.record()

    driver.cleanup()
    logging.info("Simulation finished successfully. The output file is: " +
                 db.filename)
