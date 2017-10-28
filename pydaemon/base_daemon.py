import sys
import os
import logging
import traceback
from signal import SIGTERM

from . import PIDS_PATH, LOGS_PATH, camel2snake, AlreadyStartedError, NotStartedError


class BaseDaemon:
    LOGGING_FORMAT = '[%(asctime)s] %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s - %(message)s'
    LOGGING_LEVEL = logging.INFO

    def __init__(self, config=None):
        self._config = config
        self._pid = self._get_pid()

        self._init_logger()

    def run(self):
        raise NotImplementedError()

    def start(self):
        if self._pid is None:
            if sys.platform == 'win32':
                pid = 0
            else:
                pid = os.fork()
                
            if pid == 0:
                self._set_pid()
                logging.info("daemon started")
                try:
                    self.run()
                except:
                    logging.critical(traceback.format_exc())
                finally:
                    self._del_pid()
                    logging.info("daemon stopped")
        else:
            raise AlreadyStartedError()

    def stop(self):
        if self._pid is not None:
            os.kill(self._pid, SIGTERM)
            self._del_pid()
            logging.info("daemon stopped")
        else:
            raise NotStartedError()

    def restart(self):
        self.stop()
        self.start()

    @classmethod
    def has_error(cls):
        log_dir = cls._get_log_dir()
        error_path = os.path.join(log_dir, 'error.log')
        return os.path.exists(error_path) and os.stat(error_path).st_size

    def _get_pid(self):
        pid_path = self._get_pid_path()
        if os.path.exists(pid_path):
            with open(pid_path) as f:
                return int(f.read())
        else:
            return None

    def _set_pid(self):
        pid_path = self._get_pid_path()
        self._pid = os.getpid()
        with open(pid_path, 'w') as f:
            print(self._pid, file=f)

    def _del_pid(self):
        pid_path = self._get_pid_path()
        os.remove(pid_path)
        self._pid = None

    def _get_pid_path(self):
        name = camel2snake(self.__class__.__name__)
        pid_path = os.path.join(
            PIDS_PATH,
            '{}.pid'.format(name)
        )
        return pid_path

    def _init_logger(self):
        logger = logging.getLogger()
        logger.setLevel(self.LOGGING_LEVEL)

        formatter = logging.Formatter(self.LOGGING_FORMAT)

        self._add_logging_handler(logger, formatter, 'debug')
        self._add_logging_handler(logger, formatter, 'info')
        self._add_logging_handler(logger, formatter, 'warning')
        self._add_logging_handler(logger, formatter, 'error')

    @classmethod
    def _get_log_dir(cls):
        name = camel2snake(cls.__name__)
        log_dir = os.path.join(LOGS_PATH, name)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        return log_dir

    def _add_logging_handler(self, logger, formatter, lvl):
        log_dir = self._get_log_dir()
        level = getattr(logging, lvl.upper())
        if self.LOGGING_LEVEL <= level:
            log_path = os.path.join(log_dir, '{}.log'.format(lvl))
            handler = logging.FileHandler(log_path, mode='a')
            handler.setLevel(level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
