import curses
import logging

from screens.main import Screen

logger = logging.getLogger(__name__)


class LoginScreen(Screen):
    window = None

    running = True

    key_pressed = None

    def display(self):
        logger.info("Displaying LoginScreen")

        while self.running:

            if self.key_pressed == curses.KEY_RESIZE:
                return self.next_screen()

            self.key_pressed = self.stdscr.getch()

        return "LoginScreen"
