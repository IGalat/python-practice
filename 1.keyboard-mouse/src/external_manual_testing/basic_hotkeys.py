from tapper import Tapper


def printSome() -> None:
    print("Some")

def printMore() -> None:
    print("More")


tapper = Tapper({"a": printSome, "ctrl+b": printMore})

tapper.start()
