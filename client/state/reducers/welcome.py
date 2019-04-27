import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def welcome(state=None, action=None):
    if state is None:
        state = {"selected_option": "login", "enter_pressed": False}

    if action["type"] == "welcome_set_selected_option":
        state = set_selected_option(state, action)
    elif action["type"] == "welcome_set_enter_pressed":
        state = set_enter_pressed(state, action)

    return state


def set_selected_option(state, action):
    return extend(state, {"selected_option": action["value"]})


def set_enter_pressed(state, action):
    return extend(state, {"enter_pressed": action["value"]})
