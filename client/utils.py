import curses

from api.client import ApiClient
from settings import Configuration
from state import dispatch
from state.actions.app import set_jwt_token, set_next_screen

letters_and_numbers = "abcdefghijklmnopqrstuvwxyz0123456789"
symbols = "±!@$%^&*()_+=-€#`~,.<>/?;:' |{}[]\\"


def clear_screen(scr):
    scr.clear()
    scr.refresh()


def hide_cursor():
    curses.curs_set(0)


def turn_on_mouse_detection():
    curses.mousemask(1)


def get_text_center_y_x(height, width, text):
    x = int((width // 2) - (len(text) // 2) - len(text) % 2)
    y = height // 2
    return y, x


def get_scr_dimension(scr):
    return scr.getmaxyx()


def screen_too_small(scr):

    height, width = get_scr_dimension(scr)

    min_height = 40
    min_width = 100

    return height < min_height or width < min_width


def is_input_char(ordinal, use_symbols):

    accepted_chars = letters_and_numbers

    if use_symbols:
        accepted_chars = accepted_chars + symbols

    try:
        if chr(ordinal).lower() in accepted_chars:
            return True

        return False
    except:
        return False


def trim_text(text, max_length):
    if len(text) < max_length:
        return text

    trim = "..."
    text = text[: max_length - 3]

    return text + trim


def skip_login_flow_if_necessary():
    if Configuration.ENV == "dev" and Configuration.SKIP_LOGIN:
        # if dev env, can skip the login process if needed (this could also be used to skip the login
        # for users who set their username and password in env variables but the check to see
        # what env we're in would have to change). Note: not a security issue as we auth users on the backend
        # as well so even skipping logging in wont affect anything.
        response = ApiClient().authenticate_user(
            Configuration.DEV_USERNAME, Configuration.DEV_PASSWORD
        )
        if response.status_code == 200:
            json = response.json()
            dispatch(set_jwt_token(json["access_token"]))
            dispatch(set_next_screen("HomeScreen"))
