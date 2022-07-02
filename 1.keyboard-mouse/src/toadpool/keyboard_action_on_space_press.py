import keyboard

# shift+space doesn't trigger it
# space right after another key doesn't trigger it, need to wait a bit
# unusable as fast ahk alternative. only for slooooow hotkeys

keyboard.add_hotkey("space", lambda: print("space was pressed!"))
keyboard.wait()
