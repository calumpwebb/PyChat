import curses
import datetime
import logging
from exceptions import ApplicationError

from screens.main import Screen
from state.actions.chat import set_all_conversations
from state import dispatch
from utils import get_text_center_y_x, trim_text

logger = logging.getLogger(__name__)


class ChatScreen(Screen):
    namespace = "chat"

    window = None

    key_pressed = 0

    # screens
    main_screen = None
    side_bar_screen = None
    message_screen = None
    input_screen = None
    side_bar_convos = []

    """ TODO for the class:
    
        - establish connection with server to receive updates
        
    """

    @property
    def class_name(self):
        return "ChatScreen"

    def display(self):
        if self.first_time_loading():
            # todo: maybe add a loading state here? whilst we're waiting to see what loads etc
            # todo: could be as simple as rendering 'loading' then render the rest when we're ready...
            # first time loading
            all_conversations_response = self.api_client.get_all_conversations()

            if all_conversations_response.status_code == 200:
                # todo: processing.... maybe change date here
                dispatch(set_all_conversations(all_conversations_response.json()['conversations']))
            else:
                raise ApplicationError("Unable to Retrieve All Conversations")

        while True:
            logger.info("key pressed %s", self.key_pressed)
            if self.key_pressed == curses.KEY_RESIZE:
                return self.dispatch_next_screen()

            self.draw_main_screen()
            self.draw_side_bar()
            self.draw_side_bar_title()
            self.draw_side_bar_conversations()

            self.draw_input_screen()
            self.draw_message_screen()

            self.key_pressed = self.stdscr.getch()

    def draw_main_screen(self):
        stdscr_height, stdscr_width = self.get_dimensions(self.stdscr)
        main_screen = self.stdscr.derwin(stdscr_height - 4, stdscr_width - 4, 2, 2)
        main_screen.box()
        main_screen.refresh()
        self.main_screen = main_screen

    def draw_side_bar(self):
        main_screen_height, main_screen_width = self.get_dimensions(self.main_screen)

        side_bar_screen_width = max(30, main_screen_width // 4)
        side_bar_screen = self.main_screen.derwin(
            main_screen_height, side_bar_screen_width, 0, 0
        )

        side_bar_screen.box()
        side_bar_screen.refresh()

        self.side_bar_screen = side_bar_screen

    def draw_side_bar_title(self):
        side_bar_screen_height, side_bar_screen_width = self.get_dimensions(
            self.side_bar_screen
        )
        side_bar_title = "Conversations"
        side_bar_title_y, side_bar_title_x = get_text_center_y_x(
            side_bar_screen_height, side_bar_screen_width, side_bar_title
        )

        self.side_bar_screen.addstr(2, side_bar_title_x, side_bar_title, curses.A_BOLD)
        self.side_bar_screen.refresh()

    def draw_side_bar_conversations(self):

        side_bar_screen_height, side_bar_screen_width = self.get_dimensions(
            self.side_bar_screen
        )

        state = self.get_state()

        data = state['all_conversations'] * 200

        message_height = 5

        max_height = side_bar_screen_height - 6

        conversations_to_show = data[: max_height // (message_height + 1)]

        for index, message in enumerate(conversations_to_show):
            username = message["username"]
            last_message = message["last_message"]
            last_message_date = message["sent_datetime"]
            own_message = message["own_message"]

            if own_message:
                last_message = ">> " + last_message

            username = trim_text(username, side_bar_screen_width - 12)
            last_message = trim_text(last_message, side_bar_screen_width - 9)

            side_bar_convo = self.main_screen.derwin(
                message_height,
                side_bar_screen_width - 4,
                6 + index * (message_height + 1),
                2,
            )

            side_bar_convo.box()

            side_bar_convo_height, side_bar_convo_width = self.get_dimensions(
                side_bar_convo
            )

            side_bar_convo_username_y, side_bar_convo_username_x = get_text_center_y_x(
                side_bar_convo_height, side_bar_convo_width, " {} ".format(username)
            )
            side_bar_convo.addstr(0, side_bar_convo_username_x, " {} ".format(username))

            side_bar_convo_last_message_y, side_bar_last_message_username_x = get_text_center_y_x(
                side_bar_convo_height, side_bar_convo_width, last_message
            )
            side_bar_convo.addstr(2, side_bar_last_message_username_x, last_message)

            side_bar_convo_last_message_date_y, side_bar_convo_last_message_date_x = get_text_center_y_x(
                side_bar_convo_height,
                side_bar_convo_width,
                " {} ".format(last_message_date),
            )
            side_bar_convo.addstr(
                message_height - 1,
                side_bar_convo_last_message_date_x,
                " {} ".format(last_message_date),
            )
            self.side_bar_convos.append(side_bar_convo)

        for side_bar_convo in self.side_bar_convos:
            side_bar_convo.refresh()

        self.side_bar_screen.refresh()

    def draw_message_screen(self):
        main_screen_height, main_screen_width = self.get_dimensions(self.main_screen)

        message_screen_width = main_screen_width - max(30, main_screen_width // 4) - 5

        message_screen = self.main_screen.derwin(
            main_screen_height - 8,
            message_screen_width,
            2,
            max(30, main_screen_width // 4) + 2,
        )

        message_screen.box()
        message_screen.refresh()

        self.message_screen = message_screen

    def draw_input_screen(self):

        main_screen_height, main_screen_width = self.get_dimensions(self.main_screen)

        input_screen_width = main_screen_width - max(30, main_screen_width // 4) - 5

        input_screen = self.main_screen.derwin(
            5,
            input_screen_width,
            main_screen_height - 7,
            max(30, main_screen_width // 4) + 2,
        )

        input_screen.box()
        input_screen.refresh()

        self.input_screen = input_screen
