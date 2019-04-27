import curses
import logging

from screens.main import Screen


logger = logging.getLogger(__name__)


class InviteScreen(Screen):
    namespace = "invite"

    window = None

    key_pressed = 0

    # form elements

    def display(self):

        while True:

            logger.info("key pressed %s", self.key_pressed)
            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            self.key_pressed = self.stdscr.getch()

