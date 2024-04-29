from enum import auto
from enum import Enum
from enum import unique


# enum_showcase_2 is more useful


@unique  # unique values
class Season(Enum):
    spring: int = 1
    summer: int = 2
    autumn: int = 3
    winter: int = 4


def seasonRun() -> None:
    print(Season.summer.__class__)

    # bug in intellij, infers int from here. mypy works ok, and executes correctly.
    # only happens if values are type-annotated. if just a = 1, no warnings

    # this disables this type of py inspections for one line.
    # over def, this would suppress it for the whole function

    # noinspection PyTypeChecker
    summer: Season = Season.summer
    # this line is not suppressed, and would need another type of check skip
    print(Season.summer.name, Season.summer.value)


# suppress false positive warn that auto() needs args
# noinspection PyArgumentList
class Weekday(Enum):
    monday = "left me broken"
    tuesday = "I was through with hoping"
    wednesday = auto()  # substituted for generated values, by default it's int 1,2...
    thursday = auto()


def weekdayRun() -> None:
    for day in Weekday:
        print(day.__class__, day.name, day.value)
    print("By identity: is monday still monday?", Weekday.monday is Weekday.monday)


class Fruits(Enum):
    # change auto() generation. lots of warnings from idea and mypy, but works
    def _generate_next_value_(name, start, count, last_values) -> str:
        return f"Fruit: " + name + f", ordinal {count}"

    apple = auto()
    orange = auto()
    mango = auto()
    green_apple = apple  # alias


def fruitsRun() -> None:
    for fruit in Fruits:
        print(fruit.name, fruit.value)
    my_external_value_string = Fruits.orange.value
    print(f"found by string value search: {Fruits(my_external_value_string)}")
    name_string = "apple"
    print(f"found by string name search: {Fruits[name_string]}")  # [] for name search
    name_string = "green_apple"
    print(f"found by alias {name_string}: {Fruits[name_string]}")


if __name__ == "__main__":
    seasonRun()
    print()
    weekdayRun()
    print()
    fruitsRun()
