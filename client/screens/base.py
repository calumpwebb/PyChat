import logging

from api import ApiClient
from state import dispatch, get_state
from state.actions.app import set_next_screen
from state.actions.errors import set_back_screen, set_error_message
from utils import get_scr_dimension, screen_too_small

logger = logging.getLogger(__name__)


class Screen:
    # TODO: find a way to include 'state' inside these?
    api_client = None

    namespace = "app"

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.api_client = ApiClient()

    @property
    def class_name(self):
        raise NotImplementedError(
            "class_name property must be implemented in parent class"
        )

    def display(self):
        raise NotImplementedError(
            "display function must be implemented in parent class"
        )

    @staticmethod
    def get_dimensions(screen):
        # todo: might be able to do some caching here?
        return get_scr_dimension(screen)

    def next_screen(self, screen=None):
        """
        If height or width are too small, then return 'TooSmallScreen' else we're
        going to show the next screen which is specified (or return back to the previous screen if already
        showing the 'TooSmallScreen' and screen is now large enough)
        """
        if screen_too_small(self.stdscr):
            return "TooSmallScreen"
        else:

            if screen:
                return screen
            else:
                state_history = self._get_state_history()

                # find the last non 'TooSmallScreen' page
                for x in reversed(state_history):
                    if x != "TooSmallScreen":
                        return x

        # default screen in case all else fails
        return "WelcomeScreen"

    def _get_state_history(self):
        return self.get_state("app")["screen_history"]

    def dispatch_next_screen(self, screen=None):
        """
        If no screen specified then we go to the either the TooSmallScreen or the last non TooSmallScreen.
        """
        next_screen = self.next_screen(screen=screen)
        dispatch(set_next_screen(next_screen))
        return next_screen

    def dispatch_error_next_screen(self, message, back_screen):
        dispatch(set_error_message(message))
        dispatch(set_back_screen(back_screen))
        self.dispatch_next_screen("ErrorScreen")

    def current_screen(self):
        _current_screen = self.get_state("app")["screen_history"][-1]
        logger.info("current screen is set to %s", _current_screen)
        logger.info("".join(i for i in get_state("app")["screen_history"]))
        return _current_screen

    def create_main_window(self):
        height, width = self.get_dimensions(self.stdscr)

        return self.stdscr.subwin(height - 2, width - 2, 1, 1)

    def get_state(self, namespace=None):
        if namespace:
            return get_state(namespace)
        else:
            return get_state(self.namespace)

    def first_time_loading(self):
        """ Not a very efficient thing but find out if its the first time viewing this page """

        # check that only the last 1 entry = the current one, not the last 2
        return self._get_state_history()[-2:] != [self.class_name, self.class_name]
