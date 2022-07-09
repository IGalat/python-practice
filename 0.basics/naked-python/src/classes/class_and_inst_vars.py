from typing import ClassVar, Dict, Final, final


class BasicStarship:
    captain: str = "Picard"  # instance variable with default
    damage: int  # instance variable without default
    stats: ClassVar[Dict[str, int]] = {}  # class variable
    paint: Final[
        str
    ] = "white"  # also class variable, and "final".(just warnings from ide and mypy)


def checkShip() -> None:
    enterprise = BasicStarship()
    assert enterprise.captain == "Picard"
    assert not hasattr(enterprise, "damage")

    enterprise.damage = 0
    BasicStarship.stats = {"speed": 700, "volume": 542000}
    assert enterprise.stats == BasicStarship.stats
    BasicStarship.paint = "red"  # can be reassigned. So Final is only warning on reassignment


# not even a warning from ide or mypy when reassigning. what?
@final
class MeowBot:
    sound: str = "meow"

    @classmethod
    def speak(cls) -> str:
        return cls.sound


def checkMeow() -> None:
    MeowBot.sound = "woof"
    assert "woof" == MeowBot.speak()


class BarkBot:
    sound: str = "bark"

    # mypy warns on reassignment, ide doesn't
    @final
    def speak(self) -> str:
        return self.sound


def checkBark() -> None:
    bot = MeowBot()
    bot.speak = lambda: "woof"
    assert "woof" == bot.speak()


if __name__ == "__main__":
    checkShip()
    checkMeow()
    checkBark()
