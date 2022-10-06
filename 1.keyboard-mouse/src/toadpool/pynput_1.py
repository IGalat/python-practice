from typing import Any

from pynput import keyboard


def on_press(key: Any) -> None:
    # keyboard.Controller().press(key)  # creates loop!
    try:
        print(f"alphanumeric key {key.char} pressed")
    except AttributeError:
        print(f"special key {key} pressed")


def on_release(key: Any) -> bool:
    # keyboard.Controller().release(key)  # creates loop!
    print(f"{key} released")
    if key == keyboard.Key.tab:
        # Stop listener
        return False
    return True


# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()
