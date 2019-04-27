import curses
import logging

from screens.main import Screen

logger = logging.getLogger(__name__)


class HomeScreen(Screen):
    window = None

    running = True

    key_pressed = None

    @property
    def class_name(self):
        return "HomeScreen"

    def display(self):

        while self.running:

            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            return self.dispatch_next_screen("InviteScreen")

            self.key_pressed = self.stdscr.getch()
