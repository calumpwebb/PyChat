import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def errors(state=None, action=None):
    if state is None:
        state = {"message": "", "back_screen": ""}

    if action["type"] == "error_set_error_message":
        state = set_error_message(state, action)
    elif action["type"] == "error_set_back_screen":
        state = set_back_screen(state, action)

    return state


def set_error_message(state, action):
    return extend(state, {"message": action["value"]})


def set_back_screen(state, action):
    return extend(state, {"back_screen": action["value"]})
