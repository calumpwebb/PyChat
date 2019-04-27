import curses
import logging

from screens.main import Screen
from state import dispatch
from state.actions.app import set_jwt_token
from state.actions.login import set_input_data_value, set_selected_option
from utils import get_text_center_y_x, is_input_char

logger = logging.getLogger(__name__)


class LoginScreen(Screen):
    namespace = "login"

    # TODO: this really needs to be refactored along with the setup component
    window = None

    key_pressed = 0

    # form elements
    form_win = None
    form_width = None
    form_height = None
    form_x = None
    form_y = None

    form_inputs = ["username", "password", "button"]

    @property
    def class_name(self):
        return "LoginScreen"

    def display(self):

        while True:
            logger.info("i loaded the login page")
            logger.info("key pressed %s", self.key_pressed)
            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            state = self.get_state()

            if state["selected_option"] != "button":
                # keyboard input
                if is_input_char(
                    self.key_pressed, not state["selected_option"] == "username"
                ):
                    if len(state[state["selected_option"]]) < 30:
                        dispatch(
                            set_input_data_value(
                                {
                                    "field": state["selected_option"],
                                    "value": state[state["selected_option"]]
                                    + chr(self.key_pressed),
                                }
                            )
                        )

                # delete
                if self.key_pressed == 127:
                    value = state[state["selected_option"]]
                    if len(value) > 0:
                        dispatch(
                            set_input_data_value(
                                {
                                    "field": state["selected_option"],
                                    "value": value[: len(value) - 1],
                                }
                            )
                        )
            else:
                if self.key_pressed == curses.KEY_ENTER or self.key_pressed == 10:
                    if self.can_continue():
                        return self.handle_user_login(state)

            # tab and down
            if self.key_pressed == 9 or self.key_pressed == 258:
                # find current index
                index = self.form_inputs.index(state["selected_option"])

                if index + 1 >= len(self.form_inputs):
                    index = 0
                else:
                    index += 1

                dispatch(set_selected_option(self.form_inputs[index]))

            # up
            if self.key_pressed == 259:
                index = self.form_inputs.index(state["selected_option"])

                if index - 1 < 0:
                    index = len(self.form_inputs) - 1
                else:
                    index -= 1

                dispatch(set_selected_option(self.form_inputs[index]))

            state = self.get_state()

            self.window = self.create_main_window()

            self.draw_sign_up_form(state)

            self.window.refresh()

            self.key_pressed = self.stdscr.getch()

    def draw_sign_up_form(self, state):
        height, width = self.get_dimensions(self.window)

        self.form_height = 30
        self.form_width = 60
        self.form_x = width // 2 - self.form_width // 2
        self.form_y = height // 2 - self.form_height // 2

        self.form_win = self.window.subwin(
            self.form_height, self.form_width, self.form_y, self.form_x
        )

        self.form_win.box()

        self.draw_title()

        self.draw_input_box(
            " User Name ", state["selected_option"] == "username", state["username"]
        )
        self.draw_input_box(
            " Password ",
            state["selected_option"] == "password",
            state["password"],
            hide_input=True,
            offset=5,
        )

        self.draw_continue_button(
            state["selected_option"] == "button", offset=14, enabled=self.can_continue()
        )

        self.form_win.refresh()

    def draw_title(self):
        height, width = self.get_dimensions(self.form_win)

        title = [
            " _                 _       ",
            "| |               (_)      ",
            "| |     ___   __ _ _ _ __  ",
            "| |    / _ \ / _` | | '_ \ ",
            "| |___| (_) | (_| | | | | |",
            "\_____/\___/ \__, |_|_| |_|",
            "              __/ |        ",
            "             |___/         ",
        ]

        y, x = get_text_center_y_x(height, width, title[0])
        for index, w in enumerate(title):
            self.form_win.addstr(
                # complicated but looks good
                2 + index,
                x,
                w,
                curses.A_BOLD,
            )

    def draw_continue_button(self, selected, offset=0, enabled=False):
        height, width = self.get_dimensions(self.form_win)

        button_win_height_y = self.form_y + 9 + offset
        button_win_height = 5
        button_win_width = 52

        button_win = self.form_win.subwin(
            button_win_height,
            button_win_width,
            button_win_height_y,
            self.form_x + width // 2 - button_win_width // 2,
        )

        # need this otherwise text doesn't delete properly
        button_win.erase()

        border = "#"

        if selected:
            button_win.attron(curses.A_BOLD)
            button_win.border(
                border, border, border, border, border, border, border, border
            )
            button_win.attroff(curses.A_BOLD)
        else:
            button_win.box()

        if selected:
            if enabled:
                text = "Press ENTER to login!"
            else:
                text = "All Fields Required"

            button_win.addstr(
                2, button_win_width // 2 - len(text) // 2, text, curses.A_BOLD
            )
        else:
            if enabled:
                text = "LOGIN!"
            else:
                text = "All Fields Required"

            button_win.addstr(2, button_win_width // 2 - len(text) // 2, text)
        button_win.refresh()

    def draw_input_box(self, title, selected, text, hide_input=False, offset=0):
        height, width = self.get_dimensions(self.form_win)

        input_win_height_y = self.form_y + 12 + offset
        input_win_height = 4
        input_win_width = 50

        input_win = self.form_win.subwin(
            input_win_height,
            input_win_width,
            input_win_height_y,
            self.form_x + width // 2 - input_win_width // 2,
        )

        # need this otherwise text doesn't delete properly
        input_win.erase()

        if hide_input:
            text_to_display = "*" * len(text)
        else:
            text_to_display = text

        y, x = get_text_center_y_x(input_win_height, input_win_width, title)

        text_y, text_x = get_text_center_y_x(input_win_height, input_win_width, text)

        if selected:
            input_win.attron(curses.A_BOLD)
            input_win.box()
            input_win.addstr(0, x, title)
            input_win.addstr(text_y, text_x, text_to_display)
            input_win.attroff(curses.A_BOLD)
        else:
            input_win.box()
            input_win.addstr(0, x, title)
            input_win.addstr(text_y, text_x, text_to_display)

        input_win.refresh()

    def handle_user_login(self, state):
        try:
            auth_response = self.api_client.authenticate_user(
                state["username"], state["password"]
            )

            if auth_response.status_code == 200:
                json = auth_response.json()
                dispatch(set_jwt_token(json["access_token"]))
                self.dispatch_next_screen("HomeScreen")
            elif auth_response.status_code == 401:
                self.dispatch_error_next_screen(
                    "Username or Password is incorrect!", "LoginScreen"
                )
        except Exception as e:
            logger.exception(e)
            pass

        return False

    def can_continue(self):
        state = self.get_state()

        return state["username"] != "" and state["password"] != ""
