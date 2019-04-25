import curses
import logging
from screens.base import Screen
from settings import Configuration
from utils import clear_screen, hide_cursor

logger = logging.getLogger(__name__)


class MainScreen(Screen):

    def render(self):
        logger.debug('main screen rendered')
        height, width = self.get_dimensions(self.stdscr)

        clear_screen(self.stdscr)
        hide_cursor()

        self.draw_outline()
        self.draw_title()
        self.draw_footer()
        self.stdscr.refresh()

    def draw_outline(self):
        self.stdscr.box()

    def draw_title(self):

        title = " {} {} ".format(Configuration.APP_TITLE, Configuration.VERSION)

        self.stdscr.attron(curses.A_BOLD)
        # self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(0, 2, title)
        # self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.attroff(curses.A_BOLD)

    def draw_footer(self):
        height, width = self.get_dimensions(self.stdscr)

        footer = " {} ".format(Configuration.APP_FOOTER)

        self.stdscr.addstr(height - 1, width - len(footer) - 1, footer)
