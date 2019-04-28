import logging

from pydux.extend import extend

logger = logging.getLogger(__name__)


def chat(state=None, action=None):
    if state is None:
        state = {"all_conversations": []}

    if action["type"] == "chat_set_all_conversations":
        state = set_all_conversations(state, action)

    return state


def set_all_conversations(state, action):
    return extend(state, {"all_conversations": action["value"]})

