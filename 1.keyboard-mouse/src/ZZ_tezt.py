import pprint

from key import Keys
from tap import Tap
from tap_group import TapGroup
from tapper import Tapper
from util.controller import KeyboardController

pp = pprint.PrettyPrinter(compact=True, indent=2)


def print_hw() -> None:
    print("Hello World!")


def piano() -> None:
    KeyboardController.send("hello people of earth. ipsum $(shift down)lorem$(shift up) qwerty asdfgh$(enter)$(ctrl)")


""" can add new key before other actions """
# Keys.f = Key(70)
# pp.pprint(Keys.all())

chiwawa = Tap("b", lambda: print("chiwawa!"), no_additional_keys=True)

generic = TapGroup(
    [
        chiwawa,
        Tap("ctrl+c", lambda: print("Aaaand cut!")),
        Tap((Keys.rctrl, Keys.d), lambda: print("ctrlD!"), no_additional_keys=True),
    ],
    "Generic",
)

another = TapGroup.from_dict({"C": lambda: print("CC"), "i": piano, "y": "yohoho1"}, "another")

remap = TapGroup.from_dict({"e": "r", "r": "e"}, "remap")

tapper = Tapper([generic, another, remap])

tapper.start()
