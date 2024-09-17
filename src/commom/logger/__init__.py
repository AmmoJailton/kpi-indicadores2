import logging
import os
import sys

LOG_LEVELS = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}


def get_log_level():
    return LOG_LEVELS.get(str.lower(os.environ.get("LOG_LEVEL", "info")))


logging.basicConfig(
    format="[INNOVATION-LOG] [%(funcName)s] [Line (%(lineno)d)] [%(levelname)s]: %(message)s",
    stream=sys.stdout,
    level=get_log_level(),
)

logger = logging.getLogger()
