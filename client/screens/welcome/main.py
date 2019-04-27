import curses
import logging

from screens.main import Screen
from state import dispatch, get_state
from state.actions.welcome import set_enter_pressed, set_selected_option
from utils import get_text_center_y_x

logger = logging.getLogger(__name__)


class WelcomeScreen(Screen):
    namespace = "welcome"

    window = None

    key_pressed = None

    @property
    def class_name(self):
        return "WelcomeScreen"

    def display(self):
        # TODO:
        #  some sort of rendered which takes a list of
        #  windows and renders them again for this screen?

        while True:
            logger.info("i loaded the welcome page page")
            if self.key_pressed == curses.KEY_LEFT:
                dispatch(set_selected_option("login"))

            if self.key_pressed == curses.KEY_RIGHT:
                dispatch(set_selected_option("sign-up"))

            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            if self.key_pressed == curses.KEY_ENTER or self.key_pressed == 10:
                dispatch(set_enter_pressed(True))

            state = self.get_state()

            self.window = self.create_main_window()

            self.window.box()
            self.draw_pychat_logo()

            if state["enter_pressed"]:
                dispatch(set_enter_pressed(False))

                if state["selected_option"] == "login":
                    return self.dispatch_next_screen("LoginScreen")
                else:
                    return self.dispatch_next_screen("SignUpScreen")
            else:
                self.draw_switcher(state["selected_option"])

            self.window.refresh()

            self.key_pressed = self.stdscr.getch()

    def draw_pychat_logo(self):

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

        subtitle = "An Open Source Terminal Messenger"
        subtitle_height, subtitle_width = get_text_center_y_x(height, width, subtitle)
        self.window.addstr(subtitle_height - 2, subtitle_width, subtitle)

    def draw_switcher(self, selected_option):
        height, width = self.get_dimensions(self.window)

        switcher_window_height = 5
        switcher_window_width = 50
        switcher_window_y = height // 2 + 10
        switcher_window_x = width // 2 - switcher_window_width // 2

        spacing = 4

        left_option_width = switcher_window_width // 2 - spacing
        left_option = self.window.subwin(
            switcher_window_height,
            left_option_width,
            switcher_window_y,
            switcher_window_x,
        )

        right_option_width = switcher_window_width // 2 - spacing
        right_option = self.window.subwin(
            switcher_window_height,
            right_option_width,
            switcher_window_y,
            width // 2 + spacing,
        )

        border = "#"

        if selected_option == "login":
            left_option.border(
                border, border, border, border, border, border, border, border
            )
        else:
            left_option.box()

        left_option_text = "Login"
        left_option.addstr(
            2, left_option_width // 2 - len(left_option_text) // 2, left_option_text
        )
        left_option.refresh()

        if selected_option == "sign-up":
            right_option.border(
                border, border, border, border, border, border, border, border
            )
        else:
            right_option.box()

        right_option_text = "Sign-Up"
        right_option.addstr(
            2, right_option_width // 2 - len(right_option_text) // 2, right_option_text
        )
        right_option.refresh()

    def draw_login(self):
        height, width = self.get_dimensions(self.window)

    def draw_sign_up(self):
        pass
