"""Colorful logging functinoality"""

import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

ALL = 1
TRACE = 2
TIMING = 5
OK = 22
SYSTEM = 25


def addLoggingLevel(levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present 

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       raise AttributeError('{} already defined in logging module'.format(levelName))
    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


addLoggingLevel('TRACE', TRACE)
addLoggingLevel('TIMING', TIMING)
addLoggingLevel('SYSTEM', SYSTEM)
addLoggingLevel('OK', OK)


class CustomFormatter(logging.Formatter):
    LOGFORMAT_A = "[%(levelname)s] %(message)s"
    LOGFORMAT_B = " / %(name)s - %(filename)s:%(lineno)d"
    dark = "\x1b[2;37m"
    timing = "\x1b[2;32m"
    green = "\x1b[10;32m"
    system = "\x1b[1;34m"
    ok = "\x1b[1;36m"
    grey = "\x1b[10;38m"
    yellow = "\x1b[10;33m"
    red = "\x1b[10;31m"
    bold_red = "\x1b[1;31m"
    reset = "\x1b[0m"
    FORMATS = {
        TRACE: dark + LOGFORMAT_A + LOGFORMAT_B + reset,
        TIMING: timing + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        DEBUG: grey + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        INFO: green + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        SYSTEM: system + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        OK: ok + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        WARNING: yellow + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        ERROR: red + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
        CRITICAL: bold_red + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def getLogger(name, level=ALL):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(ALL)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    _logger = getLogger("test", ALL)
    _logger.trace("trace 2")
    _logger.timing("timing 5")
    _logger.debug("debug 10")
    _logger.info("info 20")
    _logger.ok("ok 22")
    _logger.system("system 25")
    _logger.warning("warning 30")
    _logger.error("error 40")
    _logger.critical("critical 50")
    