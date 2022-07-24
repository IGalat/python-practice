import threading
import time
from timeit import default_timer as timer
from typing import Optional

import winput

# good base, reacts reliably. windows-only and no per-app though


WINPUT_PROPAGATE = 0
WINPUT_SUPPRESS = 4


def mouse_callback(event: winput.MouseEvent) -> Optional[int]:
    if event.action == 512:
        return WINPUT_PROPAGATE
    print(
        f"MOUSE: pos={event.position}, action={event.action}, time={event.time}, add={event.additional_data}, adtyp={type(event.additional_data)}"
    )
    # return WP_DONT_PASS_INPUT_ON  # would block all mouse actions
    return WINPUT_PROPAGATE


temp = 0
start_time = timer()


def keyboard_callback(event: winput.KeyboardEvent) -> Optional[int]:
    if timer() > start_time + 20:  # seconds. rescue option
        winput.stop()

    if event.action != 256:  # press ; 257 - release
        return WINPUT_PROPAGATE
    print(f" pressed VK code = {event.key}")

    if event.vkCode == winput.VK_ESCAPE:  # quit on pressing escape
        winput.stop()
    if 65 <= event.vkCode <= 69:  # a-e
        return WINPUT_PROPAGATE

    if event.vkCode == winput.VK_J:
        global temp
        threading.Thread(target=pressJ).start()
    return WINPUT_SUPPRESS


def pressJ() -> None:
    global temp  # not thread-specific, so triggering this twice won't lead to 2x cycles
    temp += 1
    if temp > 3:
        winput.stop()  # doesn't exit, as it's a diff thread
        return
    time.sleep(1)
    winput.click_key(winput.VK_J)


print("Press escape to quit")

# hook input
winput.hook_mouse(mouse_callback)
winput.hook_keyboard(keyboard_callback)

# enter message loop
winput.wait_messages()

# remove input hook
winput.unhook_mouse()
winput.unhook_keyboard()
