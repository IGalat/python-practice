import pprint

from key import Keys
from tap import Tap
from tapper import Tapper
from util.controller import Controller as Ct

pp = pprint.PrettyPrinter(compact=True, indent=2)


def print_hw() -> None:
    print("Hello World!")


def piano() -> None:
    Ct.send(
        "hello people of earth. ipsum $(shift down)lorem$(shift up) qweRty asdfgh$(enter)$(ctrl)"
    )


tapper = Tapper()

""" can add new key before other actions """


# Keys.f = Key(70)
# pp.pprint(Keys.all())


def is_npp_fore():
    return Ct.get_fore("Notepad++")


chiwawa = Tap("b", "chiwawa!", no_additional_keys=True, trigger_if=is_npp_fore)

tapper.group(
    [
        chiwawa,
        Tap("ctrl+c", lambda: print("Aaaand cut!")),
        Tap((Keys.rctrl, Keys.d), lambda: print("ctrlD!"), no_additional_keys=True),
    ],
    "Generic",
)

another = tapper.group(
    {"C": lambda: print("CC"), "i": piano, "y": "Yohoho!"},
    "another",
    trigger_if=lambda: Ct.get_open("foobar"),
)

tapper.group({"e": "r", "r": "e"}, "remap")

tapper.group(
    [
        Tap(
            "1", lambda: Ct.mouseover(1850, 1000), suppress_trigger_key_on_action=False
        ),
        Tap("2", lambda: print(Ct.get_mouse_pos())),
        Tap("delete+mmb", "Tu-Turuuu!"),
    ],
    "mouse",
)


def capsOn() -> None:
    caps = "CAPS ON" if Ct.toggled(Keys.caps) else "caps off"
    print(caps)


def altGrPressed() -> None:
    alt = "altGr PRESSED" if Ct.pressed(Keys.ralt) else "altGr not pressed!"
    print(alt)


tapper.group({"6": capsOn, "7": altGrPressed}, "key_state")

tapper.group(
    {
        "ctrl+down_arrow": lambda: tapper.suspend_groups("key_state", "remap"),
        "ctrl+up_arrow": lambda: tapper.unsuspend_groups("key_state", "remap"),
        ("ctrl", "left_arrow"): lambda: tapper.toggle_suspend_groups("Generic"),
    }
)

tapper.group(
    {"9": "$(ctrl+t)", "0": "$(alt+tab)", "-": lambda: Ct.set_fore("foobar")},
    "chrome",
    trigger_if=lambda: Ct.get_fore("chrome"),
)

tapper.start()
