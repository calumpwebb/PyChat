import curses

from screens.base import Screen


class LoginScreen(Screen):

    last_key_pressed = 0
    running = False

    def render(self):

        height, width = self.get_dimensions(self.stdscr)

        self.running = True

        while self.running:
            # think about a context manager here with running: ???
            self.window = self.create_window()

            if self.last_key_pressed != ord("q"):
                self.running = False

            self.last_key_pressed = self.stdscr.getch()

    def create_window(self):
        height, width = self.stdscr.getmaxyx()

        return curses.newwin(height, width, 0, 0)
