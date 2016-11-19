import logging
import traceback
from time import sleep
from abc import ABCMeta, abstractmethod

from Service import Service



class ServicePeriodical(Service):
    __metaclass__ = ABCMeta


    def __init__(self):
        super(ServicePeriodical, self).__init__()
        self._timeout = None


    def run(self):
        self.init()

        assert self._timeout is not None, "self._timeout is not set"

        while True:
            try:
                self.handler()
                sleep(self._timeout)

            except Exception:
                logging.error(traceback.format_exc())


    @abstractmethod
    def init(self):
        pass


    @abstractmethod
    def handler(self):
        pass
