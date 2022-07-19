import pprint

from tap import Tap
from tap_group import TapGroup
from tapper import Tapper

pp = pprint.PrettyPrinter(compact=True, indent=2)


def print_hw() -> None:
    print("Hello World!")


""" can add new key before other actions """
# Keys.f = Key(70)
# pp.pprint(Keys.all())

chiwawa = Tap("b", lambda: print("chiwawa!"))

generic = TapGroup([chiwawa, Tap("ctrl+c", lambda: print("Aaaand cut!"))], "Generic")

# another = TapGroup.from_dict({Keys.c: lambda: print("CC")}, "another")  # unhashable Keys.c
another = TapGroup.from_dict({"C": lambda: print("CC")}, "another")

tapper = Tapper([generic, another])

tapper.start()

