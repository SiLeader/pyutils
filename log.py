# Android like log system.

from logging import getLogger, config as logging_config
import logging
import enum

__logger = None


class Logger:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__logger = getLogger(identifier)

    @staticmethod
    def __level(level):
        return {
            Level.Critical.value: "C",
            Level.Error.value: "E",
            Level.Warning.value: "W",
            Level.Info.value: "I",
            Level.Debug.value: "D"
        }[level.value]

    def write(self, level, tag, msg):
        self.__logger.log(level.value, "{}: {}/{}: {}".format(self.__identifier, tag, Logger.__level(level), msg))


class Level(enum.Enum):
    Critical = logging.CRITICAL
    Error = logging.ERROR
    Warning = logging.WARNING
    Info = logging.INFO
    Debug = logging.DEBUG


def init(identifier, config_file=None, config_dict=None):
    global __logger
    if config_file is not None:
        logging_config.fileConfig(config_file)
    elif config_dict is not None:
        logging_config.dictConfig(config_dict)
    __logger = Logger(identifier)


def __write(level, tag, msg):
    if __logger is None:
        raise RuntimeError("log system not initialized. please call {}.init(identifier) function.".format(__name__))
    __logger.write(level, tag, msg)


def d(tag, msg):
    __write(Level.Debug, tag, msg)


def i(tag, msg):
    __write(Level.Info, tag, msg)


def w(tag, msg):
    __write(Level.Warning, tag, msg)


def e(tag, msg):
    __write(Level.Error, tag, msg)


def c(tag, msg):
    __write(Level.Critical, tag, msg)
