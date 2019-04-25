import curses

from screens import MainScreen
from screens.login import LoginScreen
from screens.welcome import WelcomeScreen

screens = {"login": LoginScreen}


def draw(stdscr):

    main = MainScreen(stdscr).render()
    # WelcomeScreen(stdscr).render()
    # login_screen = LoginScreen(stdscr)
    # login_screen.render()


if __name__ == "__main__":
    curses.wrapper(draw)
