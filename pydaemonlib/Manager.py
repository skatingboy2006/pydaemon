import os
import inspect
from argparse import ArgumentParser

from colorprint import tpl_red, tpl_green, tpl_empty
from models.Config import Config
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
        parser.add_argument("-c", "--config", help="name of config")
        parser.add_argument("-a", "--all", help="all services", action="store_true")

        return parser.parse_args()


    def __get_config(self, config_name):
        if config_name is not None:
            config_path = "local/%s.yaml" % config_name
        else:
            config_path = None

        return Config(config_path)


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

                if pid in os.listdir('/proc'): # checking started pid
                    started_services[service_name] = pid
                else:
                    service = Service.create(service_name, None)
                    service.remove_pidfile()

        return started_services


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
                tpl_green.format('started') if service_name in started_services else tpl_empty.format('stopped'),
                started_services[service_name] if service_name in started_services else '',
                tpl_red.format('errors') if errors else tpl_green.format('ok')
            )


    def __start(self, args):
        """
            Start a specified service
        """
        config = self.__get_config(args.config)

        if args.all:
            names = self.__get_stopped_services()
            for name in names:
                self.__start_service(name, config)

        else:
            assert args.name is not None
            self.__start_service(args.name, config)


    def __stop(self, args):
        """
            Stop a specified service
        """
        config = self.__get_config(args.config)

        if args.all:
            names = self.__get_started_services()
            for name in names:
                self.__stop_service(name, config)

        else:
            assert args.name is not None
            self.__stop_service(args.name, config)


    def __restart(self, args):
        """
            Restart a specified service
        """
        config = self.__get_config(args.config)

        if args.all:
            names = self.__get_started_services()
            for name in names:
                self.__restart_service(name, config)

        else:
            assert args.name is not None
            self.__restart_service(args.name, config)


    def __start_service(self, name, config):
        try:
            service = Service.create(name, config)
            service.start()

        except ServiceError as exc:
            print exc


    def __stop_service(self, name, config):
        try:
            service = Service.create(name, config)
            service.stop()

        except ServiceError as exc:
            print exc


    def __restart_service(self, name, config):
        try:
            service = Service.create(name, config)
            service.restart()

        except ServiceError as exc:
            print exc
