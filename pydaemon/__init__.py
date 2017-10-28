import os
import re
import importlib.util


SETTINGS_PATH = os.path.join(
    os.path.expanduser('~'),
    '.pydaemon'
)
PROJECT_NAME = os.path.split(os.path.abspath('.'))[-1]
PROJECT_PATH = os.path.join(SETTINGS_PATH, PROJECT_NAME)
PIDS_PATH = os.path.join(PROJECT_PATH, 'pids')
LOGS_PATH = os.path.join(PROJECT_PATH, 'logs')

if not os.path.exists(SETTINGS_PATH):
    os.mkdir(SETTINGS_PATH)
if not os.path.exists(PROJECT_PATH):
    os.mkdir(PROJECT_PATH)
if not os.path.exists(PIDS_PATH):
    os.mkdir(PIDS_PATH)
if not os.path.exists(LOGS_PATH):
    os.mkdir(LOGS_PATH)


class PydaemonError(Exception):
    pass


class AlreadyStartedError(PydaemonError):
    pass


class NotStartedError(PydaemonError):
    pass


def snake2camel(s):
    return ''.join(e.title() for e in s.split('_'))


def camel2snake(s):
    return re.sub(r'([A-Z])', r'_\1', s).lower()[1:]


def get_available_daemons():
    from .base_daemon import BaseDaemon

    result = {}
    for name in os.listdir('daemons'):
        match = re.match(r'([a-zA-Z0-9][a-zA-Z0-9\_]*)\.py', name)
        if match is not None:
            module_name = match.group(1)
            cls_name = snake2camel(module_name)

            spec = importlib.util.spec_from_file_location(
                module_name,
                os.path.join('daemons', name)
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, cls_name):
                cls = getattr(module, cls_name)
                if issubclass(cls, BaseDaemon):
                    result[module_name] = cls

    return result


def get_started_daemons():
    result = {}
    for name in os.listdir(PIDS_PATH):
        pid_path = os.path.join(PIDS_PATH, name)
        with open(pid_path) as f:
            pid = int(f.read())
        result[name[:-4]] = pid
    return result
