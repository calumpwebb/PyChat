import curses
import logging

from screens.main import Screen
from utils import get_text_center_y_x, trim_text, is_input_char

logger = logging.getLogger(__name__)


class ErrorScreen(Screen):
    namespace = "errors"

    window = None

    key_pressed = None

    # error window
    error_win = None
    error_win_height = None
    error_win_y = None
    error_win_width = None
    error_win_x = None

    def display(self):

        while True:
            logger.info('error menu looped')
            state = self.get_state()

            self.window = self.create_main_window()

            self.window.box()
            self.window.refresh()

            self.draw_error_box(state)

            self.window.refresh()

            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            # ESC
            if is_input_char(self.key_pressed, True):
                logger.info('i pressed esc')
                return self.dispatch_next_screen(state["back_screen"])

            self.key_pressed = self.stdscr.getch()

    def draw_error_box(self, state):
        height, width = self.get_dimensions(self.stdscr)

        self.error_win_height = height // 3
        self.error_win_y = height // 3
        self.error_win_width = width // 2
        self.error_win_x = width // 2 - self.error_win_width // 2

        # self.form_height, self.form_width, self.form_y, self.form_x
        self.error_win = self.stdscr.subwin(
            self.error_win_height, self.error_win_width, self.error_win_y, self.error_win_x
        )

        self.error_win.box()

        self.draw_title()

        self.draw_message(trim_text(state["message"], self.error_win_width - 5))
        self.draw_footer()

        self.error_win.refresh()

    def draw_title(self):
        height, width = self.get_dimensions(self.error_win)

        title = [
            "  ______                     ",
            " |  ____|                    ",
            " | |__   _ __ _ __ ___  _ __ ",
            " |  __| | '__| '__/ _ \| '__|",
            " | |____| |  | | | (_) | |   ",
            " |______|_|  |_|  \___/|_|   ",
        ]

        y, x = get_text_center_y_x(height, width, title[0])
        for index, w in enumerate(title):
            self.error_win.addstr(2 + index, x, w, curses.A_BOLD)

    def draw_message(self, message):
        height, width = self.get_dimensions(self.error_win)

        y, x = get_text_center_y_x(height, width, message)

        self.error_win.addstr(height - 4, x, message, curses.A_BOLD)

    def draw_footer(self):
        message = " Press ANY KEY to dismiss "
        height, width = self.get_dimensions(self.error_win)

        y, x = get_text_center_y_x(height, width, message)

        self.error_win.addstr(height - 1, x, message)
        self.error_win.addstr(0, x, message)
