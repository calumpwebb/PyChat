import curses


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
