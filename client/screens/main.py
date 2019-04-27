import curses
import logging

from screens.base import Screen
from utils import clear_screen, hide_cursor

logger = logging.getLogger(__name__)


class MainScreen(Screen):
    def display(self):
        clear_screen(self.stdscr)
        hide_cursor()

        self.draw_outline()
        self.draw_title()
        self.draw_current_screen_text()
        self.draw_footer()
        self.stdscr.refresh()

        return self.current_screen()

    def draw_outline(self):
        self.stdscr.box()

    def draw_title(self):

        title = " {} {} ".format("PyChat", "v1.0")

        self.stdscr.addstr(0, 2, title, curses.A_BOLD)

    def draw_footer(self):
        height, width = self.get_dimensions(self.stdscr)

        footer = " {} ".format("Developed by Calum Webb")

        self.stdscr.addstr(height - 1, width - len(footer) - 1, footer)

    def draw_current_screen_text(self):
        height, width = self.get_dimensions(self.stdscr)

        current_screen_text = " {} ".format(self.current_screen())

        self.stdscr.addstr(0, width - len(current_screen_text) - 2, current_screen_text)
