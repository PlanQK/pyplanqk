import logging

from pyplanqk.high_level_actions import *
from pyplanqk.models import *


class CustomFormatter(logging.Formatter):
    _formats = {}

    def __init__(self, *args, **kwargs):
        super(CustomFormatter, self).__init__(*args, **kwargs)

    def set_formatter(self, _level, _formatter):
        self._formats[_level] = _formatter

    def format(self, record):
        f = self._formats.get(record.levelno)

        if f is None:
            f = super(CustomFormatter, self)

        return f.format(record)


name = "pyplanqk"
level = logging.INFO

default_frmt_str = "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s"
debug_frmt_str = "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s"
info_frmt_str = "%(asctime)s | %(name)s | %(message)s"
formatter = CustomFormatter(default_frmt_str)
formatter.set_formatter(logging.DEBUG, logging.Formatter(debug_frmt_str))
formatter.set_formatter(logging.INFO, logging.Formatter(info_frmt_str))

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger(name)
logger.setLevel(level)

logger.addHandler(stream_handler)
