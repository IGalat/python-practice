from typing import Any

from pynput import keyboard


def on_press(key: Any) -> None:
    keyboard.Controller().press(key)
    try:
        print("alphanumeric key {0} pressed".format(key.char))
    except AttributeError:
        print("special key {0} pressed".format(key))


def on_release(key: Any) -> bool:
    keyboard.Controller().release(key)
    print("{0} released".format(key))
    if key == keyboard.Key.tab:
        # Stop listener
        return False
    return True


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()
