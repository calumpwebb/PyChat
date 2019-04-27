import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def invite(state=None, action=None):
    if state is None:
        state = {"all_invites": [], "selected_option": "back"}

    if action["type"] == "invite_set_all_invites":
        state = set_all_invites(state, action)
    elif action["type"] == "invite_set_selected_option":
        state = set_selected_option(state, action)

    return state


def set_all_invites(state, action):
    return extend(state, {"all_invites": action["value"]})


def set_selected_option(state, action):
    return extend(state, {"selected_option": action["value"]})
