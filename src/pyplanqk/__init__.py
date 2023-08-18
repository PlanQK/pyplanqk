import logging

from pyplanqk.high_level_actions import PyPlanQK


name = "pyplanqk"
level = logging.INFO

default_frmt_str = "%(asctime)s | [%(levelname)s] | %(name)s.%(funcName)s | %(message)s"
formatter = logging.Formatter(default_frmt_str)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger(name)
logger.setLevel(level)

logger.addHandler(stream_handler)
