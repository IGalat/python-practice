import time
from timeit import default_timer as timer

import win32api

start_time = timer()

buttons = { "lmb": 1, "rmb": 2} #{"l_alt": 164, "r_alt": 165}


def is_pressed(vk: int) -> bool:
    return win32api.GetKeyState(vk) < 0


for _ in range(100):
    for name, vk in buttons.items():
        print(f"{name} pressed? {is_pressed(vk)}")

    print()
    time.sleep(1)
