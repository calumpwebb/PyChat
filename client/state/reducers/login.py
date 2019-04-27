import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def login(state=None, action=None):
    if state is None:
        state = {
            "selected_option": "username",
            "username": "",
            "password": ""
        }

    if action["type"] == "login_set_selected_option":
        state = set_selected_option(state, action)
    elif action["type"] == "login_set_input_data_value":
        state = set_input_data_value(state, action)

    return state


def set_selected_option(state, action):
    return extend(state, {"selected_option": action["value"]})


def set_input_data_value(state, action):
    return extend(state, {action["value"]["field"]: action["value"]["value"]})
