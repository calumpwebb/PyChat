import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def app(state=None, action=None):
    if state is None:
        state = {"current_screen": "WelcomeScreen", "screen_history": ["WelcomeScreen"]}

    if action["type"] == "app_set_next_screen":
        state = set_current_screen(state, action)
    elif action["type"] == "app_set_jwt_token":
        state = set_jwt_token(state, action)

    return state


def set_jwt_token(state, action):
    return extend(state, {"jwt_token": action["value"]})


def set_current_screen(state, action):
    return extend(
        state,
        {
            "current_screen": action["value"],
            "screen_history": state["screen_history"] + [action["value"]],
        },
    )
