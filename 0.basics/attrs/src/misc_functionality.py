from typing import ClassVar, Any, Optional, Final

import attrs
from typing_extensions import Self  # will be in typing module in later python, check for that.


# factory method best practice
@attrs.frozen  # immutable, same as @define(frozen=True)
class User:
    user_id: int  # id shadows built-in name, apparently best practice to add _
    login: str
    first_name: str
    last_name: str
    age: int
    password: str

    # attributes with defaults have to be in the end. lame
    max_id: ClassVar[int] = 0
    active: bool = True

    # should be outside of class, can work for multiple classes
    # Any is a hack, User should instead have a parent class with max_id and use it here
    @staticmethod  # has no "cls", so can't use class- or static methods of cls, only explicitly User.method()
    def generate_next_id_static(clazz: Any) -> int:
        clazz.max_id += 1
        return clazz.max_id

    # better option? this has to be written per class
    @classmethod
    def generate_next_id(cls) -> int:
        cls.max_id += 1
        return cls.max_id

    """ post_init impossible on frozen class, __pre as well. lame, workaround below """

    # def __attrs_post_init__(self) -> None:
    #     User.max_id += 1
    #     self.id = User.max_id

    """
    workaround for on-creation actions. BAD example.
    string return type is hacky
    kwargs are unclear, instead use real args in normal situation
    **kwargs: Any - hack too
    """

    @classmethod
    def new_with_id(cls, **kwargs: Any) -> "User":
        return User(user_id=cls.generate_next_id(), **kwargs)  # idea warns because of cls, not User. Why?

    # still not best
    @classmethod
    def from_all_1(
        cls, login: str, first_name: str, last_name: str, age: int, password: str
    ) -> Self:  # best way to return self from any method! Py 3.11+ has it in "typing", not experimental
        # copy-pasting the names of every var to its value is ugly, tedious and error-prone, but works.
        return User(
            user_id=cls.generate_next_id(),
            login=login,
            first_name=first_name,
            last_name=last_name,
            age=age,
            password=password,
        )

    # best method? can be simplified by for instead of dict comp
    @classmethod
    def from_all_2(cls, login: str, first_name: str, last_name: str, age: int, password: str) -> Self:
        fields = locals()
        exclude_fields = ["cls"]
        kwargs_to_use = {key: fields[key] for key in fields if key not in exclude_fields}
        return cls(user_id=cls.generate_next_id(), **kwargs_to_use)

    # example with additional transformations
    # * in args means all args after have to be kw
    @classmethod
    def from_full_name(cls, *, login: str, full_name: str, password: str, age: Optional[int] = 0) -> Self:
        first_name, last_name = full_name.split(" ")

        fields = locals()  # this after transformations
        for field in ["cls", "full_name"]:  # if any intermediate variables, have to exclude them too!
            fields.pop(field)
        return cls(user_id=cls.generate_next_id(), **fields)

    @classmethod
    def userRun(cls) -> None:
        print(User.from_all_1(login="xx_PWN_xx", first_name="vasya", last_name="pupkin", age=11, password="pa55"))
        print(User.from_all_2(login="LinusT", first_name="Linus", last_name="Torwald", age=200, password="WinSucks"))
        print(User.from_full_name(login="VVV", full_name="Julius Caesar", password="DaddyCool"))


# exclude / transform fields in repr, asdict, astuple
@attrs.frozen
class Player:
    player_id: int
    login: str
    first_name: str
    # the only way to change field in repr nicely. no way to combine fields (full=first+ +last) ?
    # only works on repr, not on astuple or aslist
    last_name: str = attrs.field(repr=lambda value: Player.get_initial(value))
    age: int
    password: str

    # should be separate in util
    @staticmethod
    def get_initial(name: str) -> str:
        return name[:1].upper() + "."

    @staticmethod
    def exclude_pass(field: attrs.Attribute, value: Any) -> bool:
        return field.name not in ["password"]

    @staticmethod
    def playerRun() -> None:
        player = Player(1, "loginnn", "Jim", "Raynor", 33, "jimmityPass")
        print(player)

        print(attrs.astuple(player))
        print(attrs.asdict(player))
        player = attrs.evolve(player, first_name="Jimm")  # false positive warning
        print(attrs.asdict(player, filter=Player.exclude_pass))
        print(attrs.asdict(player, filter=lambda field, v: field.name != "password"))  # same as previous


# for Account.
def non_negative_number(instance: Any, field: attrs.Attribute, value: Any) -> None:
    if value < 0:
        e = f"{field.name} of {instance} should be non-negative!"
        # raise ValueError(e)
        print(e)


# ClassVar - good behaviour
# Converters and validators - shouldn't use, factory instead
@attrs.frozen
class Account:
    # built-in converter. I guess this is from string only
    account_id: int = attrs.field(converter=int)
    # this is much more universal. potential bugs ahoy!
    login: str = attrs.field(converter=str)

    password: str

    type: str = "User"

    # works very nicely. Actual class field, unlike naked python!
    # Ignores frozen on class, can't be final?
    description: ClassVar[str] = "Account of blahblah"

    active: bool = True

    # 2.5 ways to validate: callable(builtin or custom) and decorator
    # attrs doc: "Although your initializers should do as little as possible..."
    # probably shouldn't use validators on data classes
    credits: int = attrs.field(default=0, validator=[attrs.validators.instance_of(int), non_negative_number])

    @credits.validator
    def credits_validate(self, field: attrs.Attribute, value: Any) -> None:
        max_ = -1000
        if value > max_:
            e = f"Credits over limit of {max_}!"
            # raise ValueError(e)
            print(e)

    @staticmethod
    def accountRun() -> None:
        acc = Account("123", {"lala": "fafa"}, "l33t", type="Admin", credits=-23)
        print(acc)

        print(Account.description)
        Account.description = "new acc description"
        print(Account.description)


if __name__ == "__main__":
    User.userRun()
    print()
    Player.playerRun()
    print()
    Account.accountRun()
