import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def signup(state=None, action=None):
    if state is None:
        state = {
            "selected_option": "username",
            "username": "",
            "password": "",
            "confirm_password": "",
            "invitation_token": "",
        }

    if action["type"] == "sign_up_set_selected_option":
        state = set_selected_option(state, action)
    elif action["type"] == "sign_up_set_input_data_value":
        state = set_input_data_value(state, action)

    return state


def set_selected_option(state, action):
    return extend(state, {"selected_option": action["value"]})


def set_input_data_value(state, action):
    return extend(state, {action["value"]["field"]: action["value"]["value"]})
