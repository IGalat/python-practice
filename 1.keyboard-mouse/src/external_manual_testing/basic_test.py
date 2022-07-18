import pprint

from tapper import Tapper

pp = pprint.PrettyPrinter(compact=True, indent=2)

tapper = Tapper()

pp.pprint(tapper)
