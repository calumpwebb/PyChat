import curses
import logging

from screens.main import Screen
from utils import get_text_center_y_x

logger = logging.getLogger(__name__)


class WelcomeScreen(Screen):

    window = None

    running = True

    key_pressed = None

    option_selected = 'login'

    def display(self):
        # TODO:
        #  some sort of rendered which takes a list of
        #  windows and renders them again for this screen?
        logger.info("Displaying WelcomeScreen")

        while self.running:

            # think about a context manager here with running: ???
            self.window = self.create_main_window()

            self.window.box()
            self.window.refresh()

            self.draw_welcome_logo()

            if self.key_pressed == curses.KEY_LEFT:
                self.option_selected = 'login'

            if self.key_pressed == curses.KEY_RIGHT:
                self.option_selected = 'sign-up'

            self.draw_switcher()

            # self.draw_login_box()

            self.window.refresh()

            if self.key_pressed == ord("c"):
                return "LoginScreen"

            if self.key_pressed == curses.KEY_RESIZE:
                return self.next_screen()

            self.key_pressed = self.stdscr.getch()

    def draw_welcome_logo(self):

        height, width = self.get_dimensions(self.stdscr)

        logo = [
            "$$$$$$$\             $$$$$$\  $$\                  $$\     ",
            "$$  __$$\           $$  __$$\ $$ |                 $$ |    ",
            "$$ |  $$ |$$\   $$\ $$ /  \__|$$$$$$$\   $$$$$$\ $$$$$$\   ",
            "$$$$$$$  |$$ |  $$ |$$ |      $$  __$$\  \____$$\\\_$$  _|  ",  # had to add an extra \ because it escaped
            "$$  ____/ $$ |  $$ |$$ |      $$ |  $$ | $$$$$$$ | $$ |    ",
            "$$ |      $$ |  $$ |$$ |  $$\ $$ |  $$ |$$  __$$ | $$ |$$\ ",
            "$$ |      \$$$$$$$ |\$$$$$$  |$$ |  $$ |\$$$$$$$ | \$$$$  |",
            "\__|       \____$$ | \______/ \__|  \__| \_______|  \____/ ",
            "          $$\   $$ |                                       ",
            "          \$$$$$$  |                       Version 1.0     ",
            "           \______/                          (alpha)       ",
        ]

        y, x = get_text_center_y_x(height, width, logo[0])
        for index, w in enumerate(logo):
            self.window.addstr(
                # complicated but looks good
                y - 2 * len(logo) // 3 - len(logo) // 2 + index - 3,
                x,
                w,
                curses.A_BOLD,
            )

        subtitle = 'An Open Source Terminal Messenger'
        subtitle_height, subtitle_width = get_text_center_y_x(height, width, subtitle)
        self.window.addstr(
            subtitle_height - 2,
            subtitle_width,
            subtitle
        )

    def draw_login_box(self):
        height, width = self.get_dimensions(self.window)

        new_win_height = 15
        new_win_width = 70

        new_win = curses.newwin(
            new_win_height, new_win_width, height // 2, width // 2 - new_win_width // 2
        )

        new_win.box()
        new_win.refresh()

        login_text = " Login "
        new_win.addstr(0, new_win_width - len(login_text), login_text)
        new_win.refresh()

        return new_win

    def draw_switcher(self):
        height, width = self.get_dimensions(self.window)

        switcher_window_height = 5
        switcher_window_width = 50
        switcher_window_y = height // 2 + 10
        switcher_window_x = width // 2 - switcher_window_width // 2

        switcher_window = curses.newwin(
            switcher_window_height,
            switcher_window_width,
            switcher_window_y,
            switcher_window_x
        )

        spacing = 4

        left_option_width = switcher_window_width // 2 - spacing
        left_option = curses.newwin(
            switcher_window_height,
            left_option_width,
            switcher_window_y,
            switcher_window_x,
        )

        right_option_width = switcher_window_width // 2 - spacing
        right_option = curses.newwin(
            switcher_window_height, right_option_width, switcher_window_y, width // 2 + spacing
        )

        border = '#'

        if self.option_selected == 'login':
            left_option.border(border, border, border, border, border, border, border, border)
        else:
            left_option.box()

        left_option_text = 'Login'
        left_option.addstr(2, left_option_width // 2 - len(left_option_text) // 2, left_option_text)
        left_option.refresh()

        if self.option_selected == 'sign-up':
            right_option.border(border, border, border, border, border, border, border, border)
        else:
            right_option.box()

        right_option_text = 'Sign-Up'
        right_option.addstr(2, right_option_width // 2 - len(right_option_text) // 2, right_option_text)
        right_option.refresh()
        pass
