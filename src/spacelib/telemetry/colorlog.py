"""Colorful logging functinoality"""

import logging
from logging import DEBUG, INFO, WARNING, CRITICAL, ERROR
import time
epoch = time.time()

LOGFORMAT_A = "[%(levelname)s] %(message)s"
LOGFORMAT_B = " / %(name)s - %(filename)s:%(lineno)d"
dark = "\x1b[2;20m"
green = "\x1b[32;20m"
grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"
FORMATS = {
    logging.DEBUG: grey + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
    logging.INFO: green + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
    logging.WARNING: yellow + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
    logging.ERROR: red + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset,
    logging.CRITICAL: bold_red + LOGFORMAT_A + reset + dark + LOGFORMAT_B + reset
}


class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def getLogger(name, level=INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    _logger = getLogger("test", logging.DEBUG)
    _logger.info("info")
    _logger.debug("debug")
    _logger.warning("warning")
    _logger.error("error")
    _logger.critical("critical")
    