from enum import IntEnum, Enum, auto
from typing import Tuple


def separatorLine() -> None:
    print("--------------------------")


# members can and must be ints
# this == RomanDigits(int, Enum)
class RomanDigits(IntEnum):
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5

    @classmethod
    def romanRun(cls) -> None:
        for digit in RomanDigits:
            # can add them, since digit is int
            print(f"5 + {digit.name} = {5 + digit}")

        print(f"Class of roman digit is {RomanDigits.I.__class__}")
        # for some reason, python during runtime gives a warning for "is"
        int_one: int = 1
        print(f"digit is its corresponding int? {RomanDigits.I is int_one}")
        print(f"digit == its corresponding int? {RomanDigits.I == 1}")
        print(f"digit > int? {RomanDigits.III > 1}")


# I can create my own enums with members being of certain type: MyEnum(MyClass, Enum)
# This is awesome! Any functionality
class Endpoints(str, Enum):
    users: str = "users"  # dunno if str here helps with type check. it's tedious considering str subtype
    customers = "customers"
    pets = auto()  # doesn't work, have to manually write name to value

    @classmethod
    def endpointsRun(cls) -> None:
        print(f"users endpoint is {Endpoints.users}")
        print(f"pets endpoint is {Endpoints.pets}")


# oneliner with different creation methods
class Months:
    # for these two, "type" mixin doesn't work? Their .value is still ordinal
    FirstQuarter = Enum("FirstQuarter", "jan feb mar", type=str)
    SecondQuarter = Enum("SecondQuarter", ["apr", "may", "jun"], type=str)
    # only in these two it's what I want, and I have to set it myself, cannot make automatic value=name
    # the "type" though gives RuntimeError on assigning another type, good
    ThirdQuarter = Enum(
        "ThirdQuarter", [("jul", "jul"), ("aug", "aug"), ("spt", "spt")], type=str
    )
    FourthQuarter = Enum(
        "FourthQuarter", {"oct": "oct", "nov": "nov", "dec": "dec"}, type=str
    )

    @classmethod
    def monthsRun(cls) -> None:
        for my_enum in [
            cls.FirstQuarter,
            cls.SecondQuarter,
            cls.ThirdQuarter,
            cls.FourthQuarter,
        ]:
            for month in my_enum:
                print(
                    f"class={month.__class__}, name={month.name}, "
                    f"value={month.value}, str == ? {month == month.name}"
                )
                break  # one month per is enough


# attributes for enum members. this way is meh, next is better
class ScreenSize(Enum):
    x: int
    y: int

    # return type annotation is a crutch (forward reference), as there's no class yet
    def __new__(cls, x: int, y: int) -> "ScreenSize":
        obj = Tuple.__new__(cls)
        obj.x = x
        obj.y = y
        return obj

    smol: Tuple = (640, 480)
    weird = (1650, 1080)
    hd = (1920, 1080)
    fourK = (2560, 1440)

    @classmethod
    def screenRun(cls) -> None:
        for size in ScreenSize:
            print(f"size of {size.name} screen is {size.x} by {size.y}")


# attributes and property-functions in members. Swell!
class Planet(Enum):
    MERCURY = (3.303e23, 2.4397e6)
    VENUS = (4.869e24, 6.0518e6)
    EARTH = (5.976e24, 6.37814e6)

    def __init__(self, mass: int, radius: int) -> None:
        self.mass = mass  # in kilograms
        self.radius = radius  # in meters

    @property
    def surface_gravity(self) -> float:
        G = 6.67300e-11  # universal gravitational constant  (m3 kg-1 s-2)
        return G * self.mass / (self.radius * self.radius)

    @classmethod
    def planetRun(cls) -> None:
        for planet in Planet:
            print(
                f"{planet.name} has mass of {planet.mass} kg, radius {planet.radius} m,"
                f" and derivative surface gravity is {planet.surface_gravity}"
            )


if __name__ == "__main__":
    RomanDigits.romanRun()
    separatorLine()
    Endpoints.endpointsRun()
    separatorLine()
    Months.monthsRun()
    separatorLine()
    ScreenSize.screenRun()
    separatorLine()
    Planet.planetRun()
