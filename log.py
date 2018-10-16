#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Android like log system for Syslog.

import syslog
import enum

__identifier = None


class Level(enum.Enum):
    Critical = syslog.LOG_CRIT
    Error = syslog.LOG_ERR
    Warning = syslog.LOG_WARNING
    Info = syslog.LOG_INFO
    Debug = syslog.LOG_DEBUG


def init(identifier):
    global __identifier

    syslog.openlog(
        identifier,
        logoption=syslog.LOG_PID | syslog.LOG_PERROR,
        facility=syslog.LOG_USER
    )
    __identifier = identifier


def __level(level):
    return {
        Level.Critical.value: "C",
        Level.Error.value: "E",
        Level.Warning.value: "W",
        Level.Info.value: "I",
        Level.Debug.value: "D"
    }[level.value]


def __message(level, tag, msg):
    if __identifier is None:
        raise RuntimeError("log system not initialized. please call {}.init(identifier) function.".format(__name__))
    syslog.syslog(level.value, "{}: {}/{}: {}".format(__identifier, tag, __level(level), msg))


def d(tag, msg):
    __message(Level.Debug, tag, msg)


def i(tag, msg):
    __message(Level.Info, tag, msg)


def w(tag, msg):
    __message(Level.Warning, tag, msg)


def e(tag, msg):
    __message(Level.Error, tag, msg)


def c(tag, msg):
    __message(Level.Critical, tag, msg)
