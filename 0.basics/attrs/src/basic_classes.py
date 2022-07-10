from typing import List

import attr
import attrs


def separatorLine() -> None:
    print("--------------------------")


# don't use this, it's same as @define but different defaults and uses old "attr" package
@attr.s
class OldStyleClass:
    x: int = attr.ib()  # also old, don't use

    @classmethod
    def oldRun(cls) -> None:
        old = OldStyleClass(2)
        print(old, f" ,  {old.x}")
        old.x = "a"  # no type enforcement whatsoever, only mypy finds
        print(old)


@attrs.define
class BasicClass:
    """
    @define generates functions:
    __init__(some, more, withDefault = 1, people = [], doggos = Factory(list))
    __repr__: BasicClass(some=value, ... for every field)
    __eq__(==), __ne__(!=), __lt__(<), __le__(<=), __gt__(>), __ge__(>=)
    line above compares tuples of all values, only works if other.__class__ is self.__class__
    __hash__:  builtins.hash(tuple of all values)
    __slots__ - so no adding new fields to instance or class

    Signature:    attrs.define(maybe_cls=None, *, these=None, repr=None, hash=None, init=None, slots=True
    , frozen=False, weakref_slot=True, str=False, auto_attribs=None, kw_only=False, cache_hash=False
    , auto_exc=True, eq=None, order=False, auto_detect=True, getstate_setstate=None, on_setattr=None
    , field_transformer=None, match_args=True)
    """

    some: str

    """
    attrs.field(*, default=NOTHING, validator=None, repr=True, hash=None, init=True, metadata=None,
    converter=None, factory=None, kw_only=False, eq=None, order=None, on_setattr=None)
        z: list = field(factory=list)  is same as  z: list = Factory(list)
    """
    more: str = attrs.field()

    # only values with default isn't required in constructor
    withDefault: int = 1

    # people are shared, doggos are not
    people: List[str] = []
    doggos: List[str] = attrs.Factory(list)

    @classmethod
    def basicRun(cls) -> None:
        # pretty format for __repr__
        print(ab1 := BasicClass("a", "b", 7), " assignment with positional args")

        """
        nope, RuntimeError: 'BasicClass' object attribute 'withDefault' is read-only 
        but error only on next instance construction(ab2), not here! wtf?
        if I don't make new instances, I can do this without an error.
        """
        # BasicClass.withDefault = 2

        print(ab2 := BasicClass(some="a", more="b"), " assignment with keyword args")
        print(ab3 := BasicClass("a", more="b"), " with mixed args, if kw last")

        # all values are compared when ==
        print(f"== works on different instances? {ab3 == ab2}")  # yes
        print(f"is works on different instances? {ab3 is ab2}")  # no

        # instance is shared. OOPS
        ab1.people.append("Jory")
        assert "Jory" in ab2.people

        ab1.doggos.append("Rex")
        assert "Rex" not in ab2.doggos

        """ 
        attrs classes are slotted by default - can't add new properties
        AttributeError: 'BasicClass' object has no attribute 'x'
        """
        # ab1.x = 3

        """
        nope, fields without default are mandatory.
        BasicClass.__init__() missing 2 required positional arguments: 'some' and 'more'
        """
        # ab4 = BasicClass()


# tells to not auto-create __init__. Instead __attrs_init__() is created and
# should be called my custom __init__. Rarely required
@attrs.define(init=False)
class CustomInitActions:
    a: int
    b: int
    c: int
    ab: int
    ac: int
    bc: int

    def __attrs_pre_init__(self) -> None:
        # self.ab = int(str(self.a) + (str(self.b))) # object has no attribute 'a'
        pass

    # probably won't use though. pre- and post-init are always available
    def __init__(self, a: int, b: int, c: int, ab: int = None, ac: int = None, bc: int = None) -> None:
        # some stuff here, like super.init

        self.__attrs_init__(a, b, c, ab, ac, bc)  # mypy warns that it doesn't exist
        # fields are only available after __attrs_init__
        self.ac = int(str(self.a) + (str(self.c)))

    def __attrs_post_init__(self) -> None:
        self.bc = int(str(self.b) + (str(self.c)))

    @classmethod
    def customInitRun(cls) -> None:
        print(CustomInitActions(1, 2, 3))
        print(f"as dict:  {attrs.asdict(CustomInitActions(4, 5, 6))}")
        print(f"as tuple:  {attrs.astuple(CustomInitActions(4, 5, 6))}")


if __name__ == "__main__":
    OldStyleClass.oldRun()
    separatorLine()
    BasicClass.basicRun()
    separatorLine()
    CustomInitActions.customInitRun()
