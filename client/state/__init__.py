import logging
from logging import FileHandler, Formatter

from pydux.create_store import create_store

from state.reducers import pychat_app

PYDUX_LOG_FILE = "pydux.log"
PYDUX_LOG_LEVEL = logging.DEBUG

logger = logging.getLogger("pydux")
logger.setLevel(PYDUX_LOG_LEVEL)
logger_file_handler = FileHandler(PYDUX_LOG_FILE, "w+")
logger_file_handler.setLevel(PYDUX_LOG_LEVEL)
logger_file_handler.setFormatter(
    Formatter("%(asctime)s.%(msecs)d %(name)s: [%(levelname)s] %(message)s")
)
logger.addHandler(logger_file_handler)


# create pydux store for the whole application
store = create_store(pychat_app)


def dispatch(action):
    logger.info("[PyDux] {} dispatched {}".format(action["type"], action["value"]))
    store["dispatch"](action)


def get_state(namespace=None):
    if namespace:
        return store["get_state"]()[namespace]
    else:
        return store["get_state"]
