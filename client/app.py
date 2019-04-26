import curses
import logging

from screens.errors import TooSmallScreen
from screens.login import LoginScreen
from screens.main import MainScreen
from screens.welcome import WelcomeScreen

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
    "WelcomeScreen": WelcomeScreen,
    "LoginScreen": LoginScreen,
    "TooSmallScreen": TooSmallScreen,
}


def draw(stdscr):

    turn_on_mouse_detection()

    current_screen = "WelcomeScreen"

    screen_states_history = []

    while True:
        logger.info("Main loop ran")

        screen_states_history.append(current_screen)

        if screen_too_small(stdscr):
            screen_states_history.append('TooSmallScreen')

        current_screen = MainScreen(stdscr, screen_states_history).display()

        scr = SCREENS[current_screen]

        # display function should return the next screen
        next_screen = scr(stdscr, screen_states_history).display()

        current_screen = next_screen


if __name__ == "__main__":
    curses.wrapper(draw)
