import curses
import logging

from screens.main import Screen
from utils import get_text_center_y_x

logger = logging.getLogger(__name__)


class TooSmallScreen(Screen):
    window = None

    key_pressed = None

    def display(self):
        logger.info("Displaying TooSmallScreen")

        while True:

            self.window = self.create_main_window()

            self.window.box()
            self.window.refresh()

            self.draw_error_message()

            self.window.refresh()

            if self.key_pressed == curses.KEY_RESIZE:
                return self.next_screen()

            if self.key_pressed == curses.KEY_MOUSE:
                id, x, y, z, bstate = curses.getmouse()


            self.key_pressed = self.stdscr.getch()



    def draw_error_message(self):
        height, width = self.get_dimensions(self.stdscr)

        # error_message
        error_message = "YOUR TERMINAL WINDOW IS TOO SMALL"

        y, x = get_text_center_y_x(height, width, error_message)
        self.window.addstr(y - 3, x, error_message, curses.A_BOLD)

        # info message
        info_message = "Required: [height: 40, width: 100]"
        y, x = get_text_center_y_x(height, width, info_message)
        self.window.addstr(y - 2, x, info_message)

        # help message
        help_message = "Please resize your window"
        y, x = get_text_center_y_x(height, width, help_message)
        self.window.addstr(y + 1, x, help_message, curses.A_UNDERLINE)

        # current message
        current_message = "Current: [height: {}, width: {}]".format(height, width)
        y, x = get_text_center_y_x(height, width, current_message)
        self.window.addstr(y + 2, x, current_message)
