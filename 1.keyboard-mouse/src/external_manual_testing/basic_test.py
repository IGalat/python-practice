import pprint

from tapper import Tapper

pp = pprint.PrettyPrinter(compact=True, indent=2)

tapper = Tapper({"a": "b"})
tap_trigger = tapper.groups[1]._taps[0].trigger_key

tapper._pre_start(True)

pp.pprint(tapper)
print("\n\n\n")
pp.pprint(tap_trigger)
print(type(tap_trigger.all_vk_codes[0]))
