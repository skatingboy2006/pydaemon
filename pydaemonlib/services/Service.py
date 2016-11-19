import sys
import os
import logging
from signal import SIGTERM
from abc import ABCMeta, abstractmethod

from pydaemonlib.errors import ServiceError



class Service(object):
    __metaclass__ = ABCMeta


    pid_path = 'tmp/pydaemon'


    def __init__(self):
        self._name = self.__class__.__name__
        self._pidfile = os.path.join(self.pid_path, '%s.pid' % self._name)


    @abstractmethod
    def run(self):
        pass


    @staticmethod
    def create(name):
        module = __import__('pydaemonlib.services').services

        if name in dir(module):
            service_cls = getattr(module, name)
        else:
            raise ServiceError("Cannot find service '%s'" % name)

        return service_cls()


    @staticmethod
    def started_list():
        names = []
        for file_name in os.listdir(Service.pid_path):
            if file_name.endswith('.pid'):
                name = file_name[:-4]
                names.append(name)
        return names


    def _daemonize(self):
        # decouple threads
        pid = os.fork()

        # stop first thread
        if pid == 0:
            # write pid into pidfile
            with open(self._pidfile, 'w') as f:
                print >> f, os.getpid()

        return pid


    def start(self):
        # if daemon is started throw as error
        if os.path.exists(self._pidfile):
            with open(self._pidfile, 'r') as f:
                pid = int(f.read().strip())
            if pid in os.listdir('/proc'):
                raise ServiceError("Service is already started")

        # create and switch to daemon thread
        pid = self._daemonize()

        if pid == 0:
            # run the body of the daemon
            logging.info("Service %s started" % self._name)
            self.run()


    def stop(self):
        # check pidfile existing
        if os.path.exists(self._pidfile):
            # read pid from file
            with open(self._pidfile, 'r') as f:
                pid = int(f.read().strip())

            # remove pidfile
            self.remove_pidfile()

            # kill daemon
            os.kill(pid, SIGTERM)

        else:
            raise ServiceError("Service is not started")


    def restart(self):
        self.stop()
        self.start()


    def remove_pidfile(self):
        os.remove(self._pidfile)
