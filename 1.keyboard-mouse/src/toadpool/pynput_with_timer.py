import time
from typing import Union

from pynput import keyboard
from pynput.keyboard._base import KeyCode, Key


def on_press(key: Union[Key, KeyCode]) -> None:
    # ugly, but enums for different platforms are different and don't inherit
    if key.__class__.__name__ == "Key":
        print("special key {0} pressed".format(key))
    elif isinstance(key, KeyCode):
        print("alphanumeric key {0} pressed".format(key.char))
    else:
        raise Exception(f"Type of keypress {key} not expected")


def on_release(key: Union[Key, KeyCode]) -> bool:
    print("{0} released".format(key))
    if key == keyboard.Key.tab:
        # Stop listener
        return False
    return True  # just for mypy


with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
    time.sleep(8)
    listener.stop()

# if I wanted to restart it, would
# make another thread and launch listener from there, not main thread
