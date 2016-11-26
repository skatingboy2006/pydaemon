import os
import sys
import inspect
from argparse import ArgumentParser

if sys.platform == "win32":
    import wmi

from colorprint import red, green, empty
from errors import ServiceError
from services import Service



class Manager(object):
    def execute(self):
        args = self.__get_args()
        getattr(self, '_Manager__' + args.command)(args)


    def __get_args(self):
        parser = ArgumentParser()

        parser.add_argument("command", help="command name", choices=['list', 'start', 'stop', 'restart'])
        parser.add_argument("-n", "--name", help="name of service")
        parser.add_argument("-a", "--all", help="all services", action="store_true")

        return parser.parse_args()


    @staticmethod
    def get_available_services():
        module = __import__('pydaemonlib.services').services

        return filter(
            lambda name: name[0].isupper() and not inspect.isabstract(getattr(module, name)),
            dir(module)
        )


    def __get_started_services(self):
        started_services = {}
        for name in os.listdir(Service.pid_path):
            if name.endswith('.pid'):
                service_name = name[:-4]

                with open(os.path.join(Service.pid_path, name)) as f:
                    pid = f.read().strip()

                if pid in self.__get_all_started_pids(): # checking started pid
                    started_services[service_name] = pid
                else:
                    service = Service.create(service_name, None)
                    service.remove_pidfile()

        return started_services


    def __get_all_started_pids(self):
        if sys.platform == "win32":
            c = wmi.WMI()
            pids = [
                str(p.ProcessId)
                for p in c.Win32_Process()
                if p.CommandLine and "pydaemon.py start" in p.CommandLine
            ]
            return pids
        else:
            return os.listdir('/proc')


    def __get_stopped_services(self):
        available_services = self.get_available_services()
        started_services = self.__get_started_services()
        return list(set(available_services) - set(started_services.keys()))


    def __check_error(self, name):
        if os.path.exists('tmp/server/logs/%s' % name):
            return os.path.getsize('tmp/server/logs/%s/error.log' % name) > 0

        else:
            return False


    def __list(self, args):
        """
            List of available services with additional information
        """
        module = __import__('pydaemonlib.services').services

        available_services = self.get_available_services()
        started_services = self.__get_started_services()

        template = "%-30s%-20s%-10s%-10s"

        for service_name in available_services:
            service_cls = getattr(module, service_name)
            errors = self.__check_error(service_name)

            print template % (
                service_name,
                green('started') if service_name in started_services else empty('stopped'),
                started_services[service_name] if service_name in started_services else '',
                red('errors') if errors else green('ok')
            )


    def __start(self, args):
        """
            Start a specified service
        """
        if args.all:
            names = self.__get_stopped_services()
            for name in names:
                self.__start_service(name)

        else:
            assert args.name is not None
            self.__start_service(args.name)


    def __stop(self, args):
        """
            Stop a specified service
        """
        if args.all:
            names = self.__get_started_services()
            for name in names:
                self.__stop_service(name)

        else:
            assert args.name is not None
            self.__stop_service(args.name)


    def __restart(self, args):
        """
            Restart a specified service
        """
        if args.all:
            names = self.__get_started_services()
            for name in names:
                self.__restart_service(name)

        else:
            assert args.name is not None
            self.__restart_service(args.name)


    def __start_service(self, name):
        try:
            service = Service.create(name)
            service.start()

        except ServiceError as exc:
            print exc


    def __stop_service(self, name):
        try:
            service = Service.create(name)
            service.stop()

        except ServiceError as exc:
            print exc


    def __restart_service(self, name):
        try:
            service = Service.create(name)
            service.restart()

        except ServiceError as exc:
            print exc
