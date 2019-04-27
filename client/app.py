import curses
import logging

from screens.errors import ErrorScreen, TooSmallScreen
from screens.home import HomeScreen
from screens.main import MainScreen
from screens.signup import SignUpScreen
from screens.welcome import WelcomeScreen
from state import dispatch, get_state
from state import store as pydux_store
from state.actions.app import set_next_screen
from utils import screen_too_small, turn_on_mouse_detection

logging.basicConfig(
    filename="logfile.log",
    filemode="a",
    format="%(asctime)s.%(msecs)d %(name)s: [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)

SCREENS = {
    # errors
    "ErrorScreen": ErrorScreen,
    "TooSmallScreen": TooSmallScreen,
    # login flow
    "WelcomeScreen": WelcomeScreen,
    "SignUpScreen": SignUpScreen,
    # main app
    "HomeScreen": HomeScreen,
}

store = pydux_store


def draw(stdscr):

    turn_on_mouse_detection()

    # This loops when the screen re sizes
    while True:

        logger.info("Main Loop Executed")

        # fixes bug where on startup screen can be too small, this is appended to the states on purpose
        # so that it correctly re renders inside the MainScreen layout
        if screen_too_small(stdscr):
            dispatch(set_next_screen("TooSmallScreen"))

        # draw the MainScreen outline
        MainScreen(stdscr).display()

        current_screen = get_state("app")["current_screen"]

        # display function should dispatch current_screen
        SCREENS[current_screen](stdscr).display()


if __name__ == "__main__":
    curses.wrapper(draw)
