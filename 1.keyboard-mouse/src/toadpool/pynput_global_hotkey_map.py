from pynput import keyboard


def on_activate_h() -> None:
    print("<ctrl>+<alt>+h pressed")


def on_activate_i() -> None:
    print("<ctrl>+<alt>+i pressed")


with keyboard.GlobalHotKeys(
    {"<ctrl>+<alt>+h": on_activate_h, "<ctrl>+<alt>+i": on_activate_i}
) as h:
    h.join()
