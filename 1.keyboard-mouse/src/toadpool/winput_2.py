import winput

def keyboard_callback(event: winput.KeyboardEvent) -> int:
    # if event.action == 256:  # press ; 257 - release
    print(f" pressed VK code = {event.key}, action = {event.action}")
    return 0

winput.hook_keyboard(keyboard_callback)
winput.wait_messages()
