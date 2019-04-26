import curses
import logging

from screens.main import Screen
from settings import Configuration
from utils import get_text_center_y_x

logger = logging.getLogger(__name__)


class WelcomeScreen(Screen):

    window = None

    running = True

    key_pressed = None

    def display(self):
        logger.info("Displaying WelcomeScreen")

        while self.running:

            # think about a context manager here with running: ???
            self.window = self.create_main_window()

            self.window.box()
            self.window.refresh()

            # draw welcome screen
            self.draw_welcome_screen_text()

            self.window.refresh()

            if self.key_pressed == ord("q"):
                self.running = False

            if self.key_pressed == ord("c"):
                return "LoginScreen"

            if self.key_pressed == curses.KEY_RESIZE:
                return self.next_screen()

            self.key_pressed = self.stdscr.getch()

    def draw_welcome_screen_text(self):

        self.draw_welcome_logo_text()

        self.draw_continue_text()

    def draw_continue_text(self):
        height, width = self.get_dimensions(self.stdscr)

        continue_message = " PRESS C TO BEGIN "
        y, x = get_text_center_y_x(height, width, continue_message)
        self.window.addstr(height - 5, x, continue_message, curses.A_REVERSE)

    def draw_welcome_logo_text(self):

        height, width = self.get_dimensions(self.stdscr)

        logo = [
            "$$$$$$$\             $$$$$$\  $$\                  $$\     ",
            "$$  __$$\           $$  __$$\ $$ |                 $$ |    ",
            "$$ |  $$ |$$\   $$\ $$ /  \__|$$$$$$$\   $$$$$$\ $$$$$$\   ",
            "$$$$$$$  |$$ |  $$ |$$ |      $$  __$$\  \____$$\\\_$$  _|  ", # had to add an extra \ because it escaped
            "$$  ____/ $$ |  $$ |$$ |      $$ |  $$ | $$$$$$$ | $$ |    ",
            "$$ |      $$ |  $$ |$$ |  $$\ $$ |  $$ |$$  __$$ | $$ |$$\ ",
            "$$ |      \$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$ | \$$$$  |",
            "\__|       \____$$ | \______/ \__|  \__| \_______|  \____/ ",
            "          $$\   $$ |                                       ",
            "          \$$$$$$  |                       Version 1.0     ",
            "           \______/                          (alpha)       "
        ]

        y, x = get_text_center_y_x(height, width, logo[0])
        for index, w in enumerate(logo):
            self.window.addstr(y - len(logo)//2 + index, x - 1, w, curses.A_BOLD)
