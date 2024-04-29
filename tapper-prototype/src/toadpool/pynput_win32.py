from pynput import keyboard
from pynput import mouse


def keyboard_event_filter(msg: int, data) -> bool:
    print(f"KB: pressed VK code = {data.vkCode}, action = {msg}")
    if (msg == 257 or msg == 256) and data.vkCode == 65:  # Key Down/Up & A
        keyboard_listener._suppress = True
    else:
        keyboard_listener._suppress = False
    return True  # False means listener's on_press/on_release will be suppressed


def mouse_event_filter(msg: int, data) -> bool:
    if msg == 512:  # mouse move
        return True
    print(f"MOUSE: action = {msg}")
    return True


keyboard_listener = keyboard.Listener(win32_event_filter=keyboard_event_filter)
keyboard_listener.start()

mouse_listener = mouse.Listener(win32_event_filter=mouse_event_filter)
mouse_listener.start()

keyboard_listener.join()
