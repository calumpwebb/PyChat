class Screen:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def render(self):
        raise NotImplementedError("render function must be implemented in parent class")

    @staticmethod
    def get_dimensions(screen):
        # todo: might be able to do some caching here?
        return screen.getmaxyx()
