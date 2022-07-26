import time

import pyperclip

from config import Config
from tap import Tap
from tap_group import TapGroup
from tapper import Tapper
from util.controller import Controller as Ct

Config.controller_interval_sec = 0.005

tapper = Tapper()

# will add this last, so if any specific hotkey triggers before, this doesn't get in the way
general = TapGroup([], "general")


def open_screen_in_paint():
    Ct.release_all_keys()
    Ct.send("$(print_screen)")  # to get it in the clipboard
    time.sleep(0.1)
    Ct.send("$(windows)paint$(enter)")  # open everyone's favourite pic editor
    time.sleep(0.1)
    Ct.send("$(ctrl+v)$(esc)$(f11)")  # paste, esc to remove select, fullscreen


general.add({"shift+print_screen": open_screen_in_paint})


mouse_pos_list = []


def add_mouse_pos():
    global mouse_pos_list
    mouse_pos_list.append(Ct.get_mouse_pos())


def finish_mouse_pos():
    global mouse_pos_list
    print(mouse_pos_list)
    pyperclip.copy(str(mouse_pos_list))
    mouse_pos_list = []


general.add({  # doesn't work properly: app key opens menu on release. why?
               # "app": "_", "shift+-": "",

             # press f7 to collect mouse positions, then alt+f7 to copy list to clipboard, print and reset
             "alt+f7": finish_mouse_pos, "f7": add_mouse_pos  # if swapped, alt+f7 won't work due to ordering
             })


# only work if foobar is open but not necessarily in the front, disable if it's not.
general.add(Tap("play_pause_media", "", trigger_if=lambda: not Ct.get_open(exec="foobar")))

tapper.group({
    "ctrl+y": "$(ctrl+shift+z)"
}, "idea", trigger_if=lambda: Ct.get_fore(exec="idea"))


def youtube_and_music_swap():
    Ct.send("$(play_pause_media) ")  # will start/stop music and stop/start video


tapper.group([
    Tap("play_pause_media", youtube_and_music_swap, trigger_if=lambda: Ct.get_open(exec="foobar"))
], "chrome", trigger_if=lambda: Ct.get_fore(exec="chrome.exe"))

tapper.add_groups([general])

tapper.start()
