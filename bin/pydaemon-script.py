from argparse import ArgumentParser

import yaml
from colorama import init
from termcolor import colored

import pydaemon


# It make colors work on Windows
init()


def __get_config(config_path):
    if config_path:
        with open(config_path) as f:
            return yaml.load(f)
    else:
        return None


def action_list(args):
    available_daemons = pydaemon.get_available_daemons()
    started_daemons = pydaemon.get_started_daemons()

    for name, cls in available_daemons.items():
        state = colored('started', 'green') if name in started_daemons else 'stopped'
        pid = started_daemons.get(name, '')
        status = colored('error', 'red') if cls.has_error() else colored('ok', 'green')
        line = "{name: <20}{state: <20}{pid: <10}{status: <10}".format(
            name=name,
            state=state,
            pid=pid,
            status=status
        )
        print(line)


def action_start(args):
    available_daemons = pydaemon.get_available_daemons()
    daemon_cls = available_daemons[args.name]
    config = __get_config(args.config)
    daemon = daemon_cls(config)
    try:
        daemon.start()
        print(colored("Daemon '{}' started".format(args.name), 'green'))
    except pydaemon.AlreadyStartedError:
        print(colored("Daemon '{}' already started".format(args.name), 'red'))


def action_stop(args):
    available_daemons = pydaemon.get_available_daemons()
    daemon_cls = available_daemons[args.name]
    daemon = daemon_cls()
    try:
        daemon.stop()
        print(colored("Daemon '{}' stopped".format(args.name), 'green'))
    except pydaemon.NotStartedError:
        print(colored("Daemon '{}' not started".format(args.name), 'red'))


def action_restart(args):
    available_daemons = pydaemon.get_available_daemons()
    daemon_cls = available_daemons[args.name]
    config = __get_config(args.config)
    daemon = daemon_cls(config)
    try:
        daemon.restart()
        print(colored("Daemon '{}' restarted".format(args.name), 'green'))
    except pydaemon.NotStartedError:
        print(colored("Daemon '{}' not started".format(args.name), 'red'))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('action', choices=['list', 'start', 'stop', 'restart'])
    parser.add_argument('-n', '--name')
    parser.add_argument('-c', '--config')
    args = parser.parse_args()

    routine = globals()['action_{}'.format(args.action)]
    routine(args)
