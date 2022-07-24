import pprint

from key import Keys
from tap import Tap
from tapper import Tapper
from util.controller import Controller

pp = pprint.PrettyPrinter(compact=True, indent=2)


def print_hw() -> None:
    print("Hello World!")


def piano() -> None:
    Controller.send("hello people of earth. ipsum $(shift down)lorem$(shift up) qweRty asdfgh$(enter)$(ctrl)")


tapper = Tapper()

""" can add new key before other actions """
# Keys.f = Key(70)
# pp.pprint(Keys.all())

chiwawa = Tap("b", "chiwawa!", no_additional_keys=True)

tapper.group(
    [
        chiwawa,
        Tap("ctrl+c", lambda: print("Aaaand cut!")),
        Tap((Keys.rctrl, Keys.d), lambda: print("ctrlD!"), no_additional_keys=True),
    ],
    "Generic",
)

tapper.group({"C": lambda: print("CC"), "i": piano, "y": "Yohoho!"}, "another")

tapper.group({"e": "r", "r": "e"}, "remap")

tapper.group(
    [
        Tap("1", lambda: Controller.mouseover(1850, 1000), suppress_trigger_key_on_action=False),
        Tap("2", lambda: print(Controller.get_mouse_pos())),
        Tap("delete+mmb", "Tu-Turuuu!"),
    ],
    "mouse",
)


def capsOn() -> None:
    caps = "CAPS ON" if Controller.toggled(Keys.caps) else "caps off"
    print(caps)


def altGrPressed() -> None:
    alt = "altGr PRESSED" if Controller.pressed(Keys.ralt) else "altGr not pressed!"
    print(alt)


tapper.group({"6": capsOn, "7": altGrPressed}, "key_state")

tapper.group(
    {
        "ctrl+down_arrow": lambda: tapper.suspend_groups("key_state", "remap"),
        "ctrl+up_arrow": lambda: tapper.unsuspend_groups("key_state", "remap"),
        ("ctrl", "left_arrow"): lambda: tapper.toggle_suspend_groups("Generic")
    }
)

tapper.start()
