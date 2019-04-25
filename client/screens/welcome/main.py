import curses
import logging

from screens.main import Screen
from settings import Configuration
from utils import get_text_center_y_x

logger = logging.getLogger(__name__)


class WelcomeScreen(Screen):

    window = None
    running = False
    last_key_pressed = 0

    def render(self):

        self.running = True

        while self.running:
            # think about a context manager here with running: ???
            self.window = self.create_window()

            # remove
            self.window.box()
            self.window.refresh()

            # draw welcome screen
            self.draw_title()

            self.refresh()

            if self.last_key_pressed == ord("q"):
                self.running = False

            self.last_key_pressed = self.stdscr.getch()

    def refresh(self):
        self.window.refresh()

    def create_window(self):
        height, width = self.get_dimensions(self.stdscr)

        return curses.newwin(height - 2, width - 2, 1, 1)

    def draw_title(self):
        height, width = self.get_dimensions(self.stdscr)

        # welcome message
        welcome_message = "Welcome to"
        y, x = get_text_center_y_x(height, width, len(welcome_message))
        self.window.attron(curses.A_BOLD)
        self.window.addstr(y - 2, x, welcome_message)
        self.window.attroff(curses.A_BOLD)

        # app title
        title = Configuration.APP_TITLE
        y, x = get_text_center_y_x(height, width, len(title))
        self.window.attron(curses.A_BOLD)
        self.window.addstr(y - 1, x, title)
        self.window.attroff(curses.A_BOLD)

        # continue
        continue_message = " PRESS ANY KEY TO BEGIN "
        y, x = get_text_center_y_x(height, width, len(continue_message))
        self.window.attron(curses.A_REVERSE)
        self.window.addstr(height - 5, x, continue_message)
        self.window.attroff(curses.A_REVERSE)

        # debug
        debug = str(self.last_key_pressed)
        y, x = get_text_center_y_x(height, width, len(debug))
        self.window.attron(curses.A_REVERSE)
        self.window.addstr(y + 3, x, debug)
        self.window.attroff(curses.A_REVERSE)
