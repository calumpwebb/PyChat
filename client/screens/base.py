import curses
import logging

from utils import get_scr_dimension, screen_too_small

logger = logging.getLogger(__name__)


class Screen:
    #TODO: find a way to include 'state' inside these?

    def __init__(self, stdscr, screen_history):
        self.stdscr = stdscr
        self.screen_history = screen_history

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
            # find the last non 'TooSmallScreen' page
            for x in reversed(self.screen_history):
                logger.info("looking through screen history", x)
                if x != "TooSmallScreen":
                    return x

            # if not found at all then do this
            return "WelcomeScreen"

    def current_screen(self):
        return self.screen_history[-1]

    def create_main_window(self):
        height, width = self.get_dimensions(self.stdscr)

        return curses.newwin(height - 2, width - 2, 1, 1)
