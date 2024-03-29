import time

from pynput import keyboard
from pynput.keyboard._base import Key
from pynput.keyboard._base import KeyCode


def on_press(key: Key | KeyCode) -> None:
    # ugly, but enums for different platforms are different and don't inherit
    if key.__class__.__name__ == "Key":
        print(f"special key {key} pressed")
    elif isinstance(key, KeyCode):
        print(f"alphanumeric key {key.char} pressed")
    else:
        raise Exception(f"Type of keypress {key} not expected")


def on_release(key: Key | KeyCode) -> bool:
    print(f"{key} released")
    if key == keyboard.Key.tab:
        # Stop listener
        return False
    return True


with keyboard.Listener(
    on_press=on_press, on_release=on_release, suppress=True
) as listener:
    time.sleep(8)
    listener.stop()

# if I wanted to restart it, would
# make another thread and launch listener from there, not main thread
