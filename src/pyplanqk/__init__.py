
from pyplanqk.high_level_actions import *
from pyplanqk.models import *


name = "pyplanqk"
level = logging.INFO
logger = logging.getLogger(name)

logger.setLevel(level)
frmt_str = "%(asctime)s | [%(levelname)s] | %(name)s | %(message)s"
formatter = logging.Formatter(frmt_str)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
