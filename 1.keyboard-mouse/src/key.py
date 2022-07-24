from dataclasses import dataclass
from typing import Optional, ClassVar, Final

from util.misc import flatten_to_list


@dataclass(init=False, repr=False)
class Key:
    vk_code: Optional[int]
    vk_name: Optional[str]
    alias_for: list["Key"]
    all_vk_codes: list[int]

    def __init__(self, vk_code: Optional[int] = None, vk_name: Optional[str] = None, alias_for: Optional[list] = None):
        if alias_for is None:
            alias_for = []
        self.vk_code = vk_code
        self.vk_name = vk_name
        self.alias_for = alias_for

        if not self.vk_code and not self.alias_for:
            raise ValueError("Must either be a key or an alias")
        self.all_vk_codes = self.collect_vk_codes()

    def __repr__(self) -> str:
        desc = []
        if self.vk_code:
            desc.append(f"{self.vk_code}")
        if self.vk_name:
            desc.append(f"{self.vk_name}")
        if self.alias_for:
            desc.append(f"alias_for={self.alias_for}")
        return "Key(" + ",".join(desc) + ")"

    def get_vk_code(self) -> int:
        if self.vk_code is not None:
            return self.vk_code
        return self.alias_for[0].get_vk_code()

    def collect_vk_codes(self) -> list[int]:
        vk_lists = []
        if self.vk_code:
            vk_lists = [self.vk_code]
        if self.alias_for:
            vk_lists.extend(flatten_to_list([alias.collect_vk_codes() for alias in self.alias_for]))
        return vk_lists

    def variants(self) -> list[str]:
        return []


def get_vk(key: int | Key | str) -> int:
    int_key: int = -1  # mypy made me do it!
    if isinstance(key, int):
        int_key = key
    if isinstance(key, Key):
        int_key = key.get_vk_code()
    elif isinstance(key, str):
        found = Keys.by_str(key)
        if not found:
            raise ValueError(f"Tried to emulate press of {key}, but didn't find it in Keys.")
        int_key = found.get_vk_code()
    return int_key


@dataclass(init=False, repr=False)
class Symbol(Key):
    regular: Final[str]
    uppercase: Final[Optional[str]]

    def __init__(self, regular: str, uppercase: Optional[str], vk_code: Optional[int], vk_name: Optional[str] = None):
        super().__init__(vk_code, vk_name, None)
        self.regular = regular
        self.uppercase = uppercase

    def __repr__(self) -> str:
        desc = [super().__repr__().lstrip("Key(").rstrip(")")]
        if self.regular:
            desc.append(f"regular='{self.regular}'")
        if self.uppercase:
            desc.append(f"uppercase='{self.uppercase}'")
        return "Symbol(" + ",".join(desc) + ")"

    def variants(self) -> list[str]:
        result = [self.regular]
        if self.uppercase:
            result.append(self.uppercase)
        return result


class Letter(Symbol):
    pass


@dataclass(slots=False)
class Keys:
    _all: ClassVar[dict[str, Key]]

    @classmethod
    def all(cls) -> dict[str, Key]:
        try:
            return cls._all
        except AttributeError:
            cls._fill_all()
        return cls._all

    @classmethod
    def _fill_all(cls) -> None:
        def is_key(name: str) -> bool:
            return not name.startswith("_") and not callable(getattr(cls, name))

        cls._all = {name: value for (name, value) in vars(cls).items() if is_key(name)}

    @classmethod
    def by_vk_code(cls, vk: Optional[int]) -> Optional[Key]:
        if vk is None:
            return None
        for key in cls.all().values():
            if vk == key.vk_code:
                return key
        return None

    @classmethod
    def by_str(cls, input: Optional[str]) -> Optional[Key]:
        if input is None:
            return None
        try:
            key = cls.all()[input]
            return key
        except KeyError:
            for key in cls.all().values():
                if input in key.variants():
                    return key
            return None

    left_mouse_button = Key(1, "VK_LBUTTON")
    right_mouse_button = Key(2, "VK_RBUTTON")
    control_break = Key(3, "VK_CANCEL")
    middle_mouse_button = Key(4, "VK_MBUTTON")
    x1_mouse_button = Key(5, "VK_XBUTTON1")
    x2_mouse_button = Key(6, "VK_XBUTTON2")

    backspace = Key(8, "VK_BACK")
    tab = Symbol("	", None, 9, "VK_TAB")
    clear = Key(12, "VK_CLEAR")  # 5 (keypad without Num Lock)
    enter = Key(13, "VK_RETURN")

    scroll_wheel_up = Key(14)  # not a real vks, crutch here
    scroll_wheel_down = Key(15)

    pause = Key(19, "VK_PAUSE")
    caps_lock = Key(20, "VK_CAPITAL")

    escape = Key(27, "VK_ESCAPE")

    space = Symbol(" ", None, 32, "VK_SPACE")
    page_up = Key(33, "VK_PRIOR")
    page_down = Key(34, "VK_NEXT")
    end = Key(35, "VK_END")
    home = Key(36, "VK_HOME")
    left_arrow = Key(37, "VK_LEFT")
    up_arrow = Key(38, "VK_UP")
    right_arrow = Key(39, "VK_RIGHT")
    down_arrow = Key(40, "VK_DOWN")

    print_screen = Key(44, "VK_SNAPSHOT")
    insert = Key(45, "VK_INSERT")
    delete = Key(46, "VK_DELETE")

    zero = Symbol("0", ")", 48)
    one = Symbol("1", "!", 49)
    two = Symbol("2", "@", 50)
    three = Symbol("3", "#", 51)
    four = Symbol("4", "$", 52)
    five = Symbol("5", "%", 53)
    six = Symbol("6", "^", 54)
    seven = Symbol("7", "&", 55)
    eight = Symbol("8", "*", 56)
    nine = Symbol("9", "(", 57)

    a = Letter("a", "A", 65)
    b = Letter("b", "B", 66)
    c = Letter("c", "C", 67)
    d = Letter("d", "D", 68)
    e = Letter("e", "E", 69)
    f = Letter("f", "F", 70)
    g = Letter("g", "G", 71)
    h = Letter("h", "H", 72)
    i = Letter("i", "I", 73)
    j = Letter("j", "J", 74)
    k = Letter("k", "K", 75)
    l = Letter("l", "L", 76)
    m = Letter("m", "M", 77)
    n = Letter("n", "N", 78)
    o = Letter("o", "O", 79)
    p = Letter("p", "P", 80)
    q = Letter("q", "Q", 81)
    r = Letter("r", "R", 82)
    s = Letter("s", "S", 83)
    t = Letter("t", "T", 84)
    u = Letter("u", "U", 85)
    v = Letter("v", "V", 86)
    w = Letter("w", "W", 87)
    x = Letter("x", "X", 88)
    y = Letter("y", "Y", 89)
    z = Letter("z", "Z", 90)

    left_windows_key = Key(91, "VK_LWIN")
    right_windows_key = Key(92, "VK_RWIN")
    app = Key(93, "VK_APPS")
    sleep = Key(95, "VK_SLEEP")

    num0 = Key(96, "VK_NUMPAD0")
    num1 = Key(97, "VK_NUMPAD1")
    num2 = Key(98, "VK_NUMPAD2")
    num3 = Key(99, "VK_NUMPAD3")
    num4 = Key(100, "VK_NUMPAD4")
    num5 = Key(101, "VK_NUMPAD5")
    num6 = Key(102, "VK_NUMPAD6")
    num7 = Key(103, "VK_NUMPAD7")
    num8 = Key(104, "VK_NUMPAD8")
    num9 = Key(105, "VK_NUMPAD9")
    numpad_multiply = Key(106, "VK_MULTIPLY")
    numpad_add = Key(107, "VK_ADD")
    separator = Key(108, "VK_SEPARATOR")  # ??
    numpad_subtract = Key(109, "VK_SUBTRACT")
    decimal = Key(110, "VK_DECIMAL")  # ??
    numpad_divide = Key(111, "VK_DIVIDE")
    f1 = Key(112, "VK_F1")
    f2 = Key(113, "VK_F2")
    f3 = Key(114, "VK_F3")
    f4 = Key(115, "VK_F4")
    f5 = Key(116, "VK_F5")
    f6 = Key(117, "VK_F6")
    f7 = Key(118, "VK_F7")
    f8 = Key(119, "VK_F8")
    f9 = Key(120, "VK_F9")
    f10 = Key(121, "VK_F10")
    f11 = Key(122, "VK_F11")
    f12 = Key(123, "VK_F12")
    f13 = Key(124, "VK_F13")
    f14 = Key(125, "VK_F14")
    f15 = Key(126, "VK_F15")
    f16 = Key(127, "VK_F16")
    f17 = Key(128, "VK_F17")
    f18 = Key(129, "VK_F18")
    f19 = Key(130, "VK_F19")
    f20 = Key(131, "VK_F20")
    f21 = Key(132, "VK_F21")
    f22 = Key(133, "VK_F22")
    f23 = Key(134, "VK_F23")
    f24 = Key(135, "VK_F24")

    num_lock = Key(144, "VK_NUMLOCK")
    scroll_lock = Key(145, "VK_SCROLL")

    left_shift = Key(160, "VK_LSHIFT")
    right_shift = Key(161, "VK_RSHIFT")
    left_control = Key(162, "VK_LCONTROL")
    right_control = Key(163, "VK_RCONTROL")
    left_alt = Key(164, "VK_LMENU")
    right_alt = Key(165, "VK_RMENU")

    # ??
    browser_back = Key(166, "VK_BROWSER_BACK")
    browser_forward = Key(167, "VK_BROWSER_FORWARD")
    browser_refresh = Key(168, "VK_BROWSER_REFRESH")
    browser_stop = Key(169, "VK_BROWSER_STOP")
    browser_search = Key(170, "VK_BROWSER_SEARCH")
    browser_favorites = Key(171, "VK_BROWSER_FAVORITES")
    browser_start_and_home = Key(172, "VK_BROWSER_HOME")

    volume_mute = Key(173, "VK_VOLUME_MUTE")
    volume_down = Key(174, "VK_VOLUME_DOWN")
    volume_up = Key(175, "VK_VOLUME_UP")
    next_track = Key(176, "VK_MEDIA_NEXT_TRACK")
    previous_track = Key(177, "VK_MEDIA_PREV_TRACK")
    stop_media = Key(178, "VK_MEDIA_STOP")
    play_pause_media = Key(179, "VK_MEDIA_PLAY_PAUSE")
    start_mail = Key(180, "VK_LAUNCH_MAIL")
    select_media = Key(181, "VK_LAUNCH_MEDIA_SELECT")
    start_application_1 = Key(182, "VK_LAUNCH_APP1")
    start_application_2 = Key(183, "VK_LAUNCH_APP2")

    semicolon = Symbol(";", ":", 186, "VK_OEM_1")
    equals = Symbol("=", "+", 187, "VK_OEM_PLUS")
    comma = Symbol(",", "<", 188, "VK_OEM_COMMA")
    minus = Symbol("-", "_", 189, "VK_OEM_MINUS")
    period = Symbol(".", ">", 190, "VK_OEM_PERIOD")
    slash = Symbol("/", "?", 191, "VK_OEM_2")
    backtick = Symbol("`", "~", 192, "VK_OEM_3")
    square_bracket_open = Symbol("[", "{", 219, "VK_OEM_4")
    backslash = Symbol("\\", "|", 220, "VK_OEM_5")
    square_bracket_close = Symbol("]", "}", 221, "VK_OEM_6")
    quote = Symbol("'", '"', 222, "VK_OEM_7")

    attn = Key(246, "VK_ATTN")
    crsel = Key(247, "VK_CRSEL")
    exsel = Key(248, "VK_EXSEL")
    erase_eof = Key(249, "VK_EREOF")
    play = Key(250, "VK_PLAY")
    zoom = Key(251, "VK_ZOOM")
    pa1 = Key(253, "VK_PA1")
    oem_clear = Key(254, "VK_OEM_CLEAR")

    # ALIAS
    lmb = left_mouse_button
    rmb = right_mouse_button
    mmb = middle_mouse_button
    x1mb = x1_mouse_button
    x2mb = x2_mouse_button
    scroll_up = scroll_wheel_up
    wheel_up = scroll_wheel_up
    scroll_down = scroll_wheel_down
    wheel_down = scroll_wheel_down

    caps = caps_lock
    esc = escape
    ins = insert
    windows = Key(alias_for=[left_windows_key, right_windows_key])

    lshift = left_shift
    rshift = right_shift
    shift = Key(vk_name="VK_SHIFT", alias_for=[left_shift, right_shift])  # vk 16, but for win os it's equal to lshift
    lcontrol = left_control
    lctrl = left_control
    rcontrol = right_control
    rctrl = right_control
    ctrl = Key(vk_name="VK_CONTROL", alias_for=[left_control, right_control])  # vk 17
    lalt = left_alt
    ralt = right_alt
    alt = Key(vk_name="VK_MENU", alias_for=[left_alt, right_alt])  # vk 18

    dash = minus
    hyphen = minus
    dot = period
