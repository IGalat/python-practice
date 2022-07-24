import pprint

from key import Keys
from tap import Tap
from tap_group import TapGroup
from tapper import Tapper
from util.controller import Controller

pp = pprint.PrettyPrinter(compact=True, indent=2)


def print_hw() -> None:
    print("Hello World!")


def piano() -> None:
    Controller.send("hello people of earth. ipsum $(shift down)lorem$(shift up) qwerty asdfgh$(enter)$(ctrl)")


""" can add new key before other actions """
# Keys.f = Key(70)
# pp.pprint(Keys.all())

chiwawa = Tap("b", "chiwawa!", no_additional_keys=True)

generic = TapGroup(
    [
        chiwawa,
        Tap("ctrl+c", lambda: print("Aaaand cut!")),
        Tap((Keys.rctrl, Keys.d), lambda: print("ctrlD!"), no_additional_keys=True),
    ],
    "Generic",
)

another = TapGroup.from_dict({"C": lambda: print("CC"), "i": piano, "y": "Yohoho!"}, "another")

remap = TapGroup.from_dict({"e": "r", "r": "e"}, "remap")

mouse = TapGroup(
    [Tap("1", lambda: Controller.mouseover(1850, 1000)), Tap("2", lambda: print(Controller.get_mouse_pos())),
     Tap("delete+mmb", "Tu-Turuuu!")], "mouse"
)

tapper = Tapper([generic, another, remap, mouse])

tapper.start()
