from typing import ClassVar, Dict, Final, final


class BasicStarship:
    captain: str = "Picard"  # class variable; also instance default
    damage: int  # instance variable without default
    stats: ClassVar[Dict[str, int]] = {}  # class variable. NOT REALLY
    # also class var, and "final" (just warnings from ide and mypy)
    paint: Final[str] = "white"


def checkShip() -> None:
    # Final can be reassigned. So it's only warning on reassignment
    BasicStarship.paint = "red"  #

    enterprise = BasicStarship()
    # correctly set instance from default
    assert enterprise.captain == BasicStarship.captain == "Picard"

    # class value stays
    enterprise.captain = "Me"
    assert enterprise.captain != BasicStarship.captain == "Picard"

    # new default changes new instances value
    BasicStarship.captain = "Shepard"
    normandy = BasicStarship()
    assert normandy.captain == "Shepard"

    assert not hasattr(enterprise, "damage")

    # NOPE! if assigned to instance - stays with instance
    enterprise.stats = {"speed": 700, "volume": 542000}
    assert enterprise.stats != normandy.stats == BasicStarship.stats

    # changing this on class changes it for instances that weren't reassigned
    # so, instance has shadow property "was 'stats' reassigned"?
    # because I changed the whole "stats" here, not just internals like adding to dict
    BasicStarship.stats = {"speed": 200}
    assert normandy.stats == BasicStarship.stats != enterprise.stats


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
    print()
    checkMeow()
    print()
    checkBark()
