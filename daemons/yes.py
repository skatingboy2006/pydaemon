import logging
from time import sleep

from pydaemon.base_daemon import BaseDaemon


class Yes(BaseDaemon):
    def run(self):
        while True:
            logging.info("yes")
            sleep(1)
