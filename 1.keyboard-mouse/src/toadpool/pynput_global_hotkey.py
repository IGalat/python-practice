from typing import Callable, Any

from pynput import keyboard


def on_activate() -> None:
    print("Global hotkey activated!")


# Note that keys are passed through pynput.keyboard.Listener.canonical
# before being passed to the HotKey instance.
# This is to remove any modifier state from the key events,
# and to normalise modifiers with more than one physical button.
def for_canonical(f: Any) -> Callable:
    return lambda k: f(listener.canonical(k))


hotkeyH = keyboard.HotKey(keyboard.HotKey.parse("<shift>+h"), on_activate)
listener = keyboard.Listener(on_press=for_canonical(hotkeyH.press), on_release=for_canonical(hotkeyH.release))
listener.start()

hotkeyG = keyboard.HotKey(keyboard.HotKey.parse("<shift>+g"), on_activate)
listener = keyboard.Listener(
    on_press=for_canonical(hotkeyG.press), on_release=for_canonical(hotkeyG.release), suppress=True
)
listener.start()

listener.join()  # without it program will exit as main thread is done and they are daemons
