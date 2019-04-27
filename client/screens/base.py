import curses
import logging

from state import dispatch, get_state
from state.actions.app import set_next_screen
from utils import get_scr_dimension, screen_too_small

logger = logging.getLogger(__name__)


class Screen:
    # TODO: find a way to include 'state' inside these?

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def display(self):
        raise NotImplementedError(
            "display function must be implemented in parent class"
        )

    @staticmethod
    def get_dimensions(screen):
        # todo: might be able to do some caching here?
        return get_scr_dimension(screen)

    def next_screen(self):
        """
        If height or width are too small, then return 'TooSmallScreen' else we're
        going to show the next screen which is specified (or return back to the previous screen if already
        showing the 'TooSmallScreen' and screen is now large enough)
        """
        if screen_too_small(self.stdscr):
            return "TooSmallScreen"
        else:

            state_history = get_state("app")["screen_history"]

            # find the last non 'TooSmallScreen' page
            for x in reversed(state_history):
                if x != "TooSmallScreen":
                    return x

            # if not found at all then do this
            return "WelcomeScreen"

    def dispatch_next_screen(self):
        next_screen = self.next_screen()
        dispatch(set_next_screen(next_screen))
        return next_screen

    @staticmethod
    def current_screen():
        _current_screen = get_state("app")["screen_history"][-1]
        logger.info("current screen is set to %s", _current_screen)
        logger.info("".join(i for i in get_state("app")["screen_history"]))
        return _current_screen

    def create_main_window(self):
        height, width = self.get_dimensions(self.stdscr)

        return self.stdscr.subwin(height - 2, width - 2, 1, 1)
