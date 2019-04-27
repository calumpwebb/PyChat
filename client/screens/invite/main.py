import curses
import datetime
import logging
from exceptions import ApplicationError

from screens.main import Screen
from state import dispatch
from state.actions.invite import set_all_invites, set_selected_option
from utils import get_text_center_y_x, trim_text

logger = logging.getLogger(__name__)


class InviteScreen(Screen):
    namespace = "invite"

    window = None

    key_pressed = 0

    # screens
    main_screen = None
    table_screen = None

    # buttons
    buttons = ["back", "invite"]

    @property
    def class_name(self):
        return "InviteScreen"

    def display(self):
        if self.first_time_loading():
            self.get_all_tokens()

        while True:
            logger.info("key pressed %s", self.key_pressed)
            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            if self.handle_key_presses():
                return

            self.draw_main_screen()
            self.draw_table_screen()
            self.draw_table_contents()

            self.draw_back_button()
            self.draw_invite_button()

            self.key_pressed = self.stdscr.getch()

    def get_all_tokens(self):
        response = self.api_client.get_all_tokens()

        # todo: deal with others?
        if response.status_code == 200:
            all_invites = response.json()

            self.process_data(all_invites)

            dispatch(set_all_invites(all_invites))
        else:
            raise ApplicationError("get_all_tokens responded with non 200 status code")

    def handle_key_presses(self):
        state = self.get_state()

        # tab and down
        if self.key_pressed == 9 or self.key_pressed == 261:
            # find current index
            index = self.buttons.index(state["selected_option"])

            if index + 1 >= len(self.buttons):
                index = 0
            else:
                index += 1

            dispatch(set_selected_option(self.buttons[index]))

        # up
        if self.key_pressed == 260:
            index = self.buttons.index(state["selected_option"])

            if index - 1 < 0:
                index = len(self.buttons) - 1
            else:
                index -= 1

            dispatch(set_selected_option(self.buttons[index]))

        state = self.get_state()

        if self.key_pressed == curses.KEY_ENTER or self.key_pressed == 10:
            if state["selected_option"] == "back":
                # todo: GO BACK A SCREEN! (not sure what screen yet)
                raise NotImplementedError("Not implemented back button on invite page")
            elif state["selected_option"] == "invite":
                # todo: get new token!
                response = self.api_client.get_new_token()

                if response.status_code == 200:
                    self.get_all_tokens()

                elif response.status_code == 429:
                    self.dispatch_error_next_screen(
                        "Only 10 tokens per day can be generated", "InviteScreen"
                    )
                    return True

        return False

    def draw_main_screen(self):
        stdscr_height, stdscr_width = self.get_dimensions(self.stdscr)
        main_screen = self.stdscr.derwin(stdscr_height - 4, stdscr_width - 4, 2, 2)
        main_screen.box()
        main_screen.refresh()
        self.main_screen = main_screen

    def draw_table_screen(self):
        main_screen_height, main_screen_width = self.get_dimensions(self.main_screen)

        table_height = main_screen_height - 10
        table_width = main_screen_width - 15
        table_start_y = 2
        table_start_x = main_screen_width // 2 - table_width // 2 - 1

        table_screen = self.main_screen.derwin(
            table_height, table_width, table_start_y, table_start_x
        )

        table_screen.box()
        table_screen.refresh()

        self.table_screen = table_screen

    def draw_table_contents(self):
        state = self.get_state()

        all_invites = state["all_invites"]

        table_screen_height, table_screen_width = self.get_dimensions(self.table_screen)

        table_height = table_screen_height - 4
        table_width = table_screen_width - 8

        # pull out into a function in utils
        self.draw_table_title(table_screen_height, table_screen_width)

        self.draw_table_headers(
            ["Token", "Created Date", "User", "Used Date"], table_width, center=True
        )

        self.draw_table_rows(
            ["token", "created_datetime", "token_user_username", "used_datetime"],
            all_invites,
            table_width,
            table_height,
            center=True,
        )

    def draw_table_title(self, height, width):
        # could do in for loop but want different behaviour for final one

        title_text_1 = "Invite users to PyChat by generating an invite token"
        title_text_2 = "below and giving it to them when they sign up"

        title_text_3 = "(max 10 per account per day)"

        title_1_y, title_1_x = get_text_center_y_x(height, width, title_text_1)
        title_2_y, title_2_x = get_text_center_y_x(height, width, title_text_2)
        title_3_y, title_3_x = get_text_center_y_x(height, width, title_text_3)

        self.table_screen.addstr(2, title_1_x, title_text_1, curses.A_STANDOUT)
        self.table_screen.addstr(3, title_2_x, title_text_2, curses.A_STANDOUT)
        self.table_screen.addstr(height - 3, title_3_x, title_text_3, curses.A_STANDOUT)

    def draw_table_headers(self, headers, width, center=False):

        # pull out into a function in utils

        header_text = ""
        column_width = width // len(headers)

        for head in headers:
            # trim down if too long
            if len(head) >= column_width - 2:
                head = trim_text(head, column_width - 1)

            if center:
                header_text += head.center(column_width)
            else:
                remaining_char = column_width - len(head)
                header_text += head + " " * remaining_char

        self.table_screen.addstr(6, 4, header_text, curses.A_BOLD)
        self.table_screen.refresh()

    def draw_table_rows(self, headers, data, width, height, center=False):

        # pull out into a function in utils
        # todo: height

        for index, row in enumerate(data):
            row_text = ""
            column_width = width // len(headers)

            for head in headers:

                data = row[head]

                # trim down if too long
                if len(data) >= column_width - 2:
                    data = trim_text(data, column_width - 1)

                if center:
                    row_text += data.center(column_width)
                else:
                    remaining_char = column_width - len(data)
                    row_text += data + " " * remaining_char

            self.table_screen.addstr(8 + index, 4, row_text)

        self.table_screen.refresh()

    @staticmethod
    def process_data(data):
        copied_data = data.copy()
        # todo: localize dates?

        for elem in copied_data:
            if not elem["used_datetime"]:
                elem["used_datetime"] = ""

            elem["token_user_username"] = (
                elem["token_user_username"] if elem["token_user_username"] else ""
            )

            # todo: used datetime
        return copied_data

    def draw_back_button(self):
        state = self.get_state()
        main_screen_height, main_screen_width = self.get_dimensions(self.main_screen)

        back_button_height = 5
        back_button_width = 30
        back_button_y = main_screen_height - 7
        back_button_x = (-back_button_width // 2) + main_screen_width // 3

        back_button = self.main_screen.derwin(
            back_button_height, back_button_width, back_button_y, back_button_x
        )

        back_button.erase()

        if state["selected_option"] == "back":
            border = "#"
            back_button.border(
                border, border, border, border, border, border, border, border
            )
            text = "Press ENTER to go BACK"
            back_text_y, back_text_x = get_text_center_y_x(
                back_button_height, back_button_width, text
            )
            back_button.addstr(back_text_y, back_text_x, text, curses.A_BOLD)
        else:
            back_button.box()
            text = "BACK"
            back_text_y, back_text_x = get_text_center_y_x(
                back_button_height, back_button_width, text
            )
            back_button.addstr(back_text_y, back_text_x, text, curses.A_BOLD)

        back_button.refresh()

    def draw_invite_button(self):
        state = self.get_state()
        main_screen_height, main_screen_width = self.get_dimensions(self.main_screen)

        invite_button_height = 5
        invite_button_width = 30
        invite_button_y = main_screen_height - 7
        invite_button_x = (-invite_button_width // 2) + (main_screen_width * 2) // 3

        invite_button = self.main_screen.derwin(
            invite_button_height, invite_button_width, invite_button_y, invite_button_x
        )

        invite_button.erase()

        if state["selected_option"] == "invite":
            border = "#"
            invite_button.border(
                border, border, border, border, border, border, border, border
            )
            text = "Press ENTER to INVITE"
            invite_text_y, invite_text_x = get_text_center_y_x(
                invite_button_height, invite_button_width, text
            )
            invite_button.addstr(invite_text_y, invite_text_x, text, curses.A_BOLD)
        else:
            invite_button.box()
            text = "INVITE"
            invite_text_y, invite_text_x = get_text_center_y_x(
                invite_button_height, invite_button_width, text
            )
            invite_button.addstr(invite_text_y, invite_text_x, text, curses.A_BOLD)

        invite_button.refresh()
