import ctypes

import winput

# scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
#
# print(scaleFactor)

# better newer api, but not in ctypes
# ctypes.windll.user32.SetProcessDpiAwarenessContext(-2)

ctypes.windll.shcore.SetProcessDpiAwareness(2)

print(winput.get_mouse_pos())
