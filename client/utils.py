import curses


def clear_screen(scr):
    scr.clear()
    scr.refresh()


def hide_cursor():
    curses.curs_set(0)


def get_text_center_y_x(height, width, text_length):
    x = int((width // 2) - (text_length // 2) - text_length % 2)
    y = height // 2
    return y, x
