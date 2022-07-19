from dataclasses import dataclass, field
from typing import Optional, ClassVar

from util.misc import flatten_to_list


@dataclass(repr=False)
class Key:
    vk_code: Optional[int] = None
    vk_name: Optional[str] = None
    input_variants: Optional[list[str]] = None
    alias_for: list["Key"] = field(default_factory=list)
    all_vk_codes: list[int] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not self.vk_code and not self.alias_for:
            raise ValueError("Must either be a key or an alias")
        self.all_vk_codes = self.collect_vk_codes()

    def __repr__(self) -> str:
        desc = []
        if self.vk_code:
            desc.append(f"{self.vk_code}")
        if self.vk_name:
            desc.append(f"{self.vk_name}")
        if self.input_variants:
            desc.append("input_variants={self.input_variants}")
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


@dataclass(slots=False)
class Keys:
    _all: ClassVar[dict]

    @classmethod
    def all(cls) -> dict:
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
        for key in cls.all():
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
        except AttributeError:
            for key in cls.all():
                input_variants = key.input_variants
                if input_variants and input in input_variants:
                    return key
            return None

    left_mouse_button = Key(1, "VK_LBUTTON")
    right_mouse_button = Key(2, "VK_RBUTTON")
    control_break = Key(3, "VK_CANCEL")
    middle_mouse_button = Key(4, "VK_MBUTTON")
    x1_mouse_button = Key(5, "VK_XBUTTON1")
    x2_mouse_button = Key(6, "VK_XBUTTON2")

    backspace = Key(8, "VK_BACK")
    tab = Key(9, "VK_TAB", input_variants=["	"])
    clear = Key(12, "VK_CLEAR")  # 5 (keypad without Num Lock)
    enter = Key(13, "VK_RETURN")

    pause = Key(19, "VK_PAUSE")
    caps_lock = Key(20, "VK_CAPITAL")

    escape = Key(27, "VK_ESCAPE")

    space = Key(32, "VK_SPACE", input_variants=[" "])
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
    delete = Key(46, "VK_DELETE", input_variants=["del"])

    zero = Key(48, input_variants=["0"])
    one = Key(49, input_variants=["1"])
    two = Key(50, input_variants=["2"])
    three = Key(51, input_variants=["3"])
    four = Key(52, input_variants=["4"])
    five = Key(53, input_variants=["5"])
    six = Key(54, input_variants=["6"])
    seven = Key(55, input_variants=["7"])
    eight = Key(56, input_variants=["8"])
    nine = Key(57, input_variants=["9"])

    a = Key(65)
    b = Key(66)
    c = Key(67)
    d = Key(68)
    e = Key(69)
    f = Key(70)
    g = Key(71)
    h = Key(72)
    i = Key(73)
    j = Key(74)
    k = Key(75)
    l = Key(76)
    m = Key(77)
    n = Key(78)
    o = Key(79)
    p = Key(80)
    q = Key(81)
    r = Key(82)
    s = Key(83)
    t = Key(84)
    u = Key(85)
    v = Key(86)
    w = Key(87)
    x = Key(88)
    y = Key(89)
    z = Key(90)

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
    browser_bac = Key(166, "VK_BROWSER_BACK")
    browser_forward = Key(167, "VK_BROWSER_FORWARD")
    browser_refresh = Key(168, "VK_BROWSER_REFRESH")
    browser_stop = Key(169, "VK_BROWSER_STOP")
    browser_search = Key(170, "VK_BROWSER_SEARCH")
    browser_favorites = Key(171, "VK_BROWSER_FAVORITES")
    browser_start_and_hom = Key(172, "VK_BROWSER_HOME")

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

    semicolon = Key(186, "VK_OEM_1", input_variants=[";"])
    equals = Key(187, "VK_OEM_PLUS", input_variants=["="])
    comma = Key(188, "VK_OEM_COMMA", input_variants=[","])
    minus = Key(189, "VK_OEM_MINUS", input_variants=["-"])
    period = Key(190, "VK_OEM_PERIOD", input_variants=["."])
    slash = Key(191, "VK_OEM_2", input_variants=["/"])
    backtick = Key(192, "VK_OEM_3", input_variants=["`"])
    square_bracket_open = Key(219, "VK_OEM_4", input_variants=["["])
    backslash = Key(220, "VK_OEM_5", input_variants=["\\"])
    square_bracket_close = Key(221, "VK_OEM_6", input_variants=["]"])
    quote = Key(222, "VK_OEM_7", input_variants=["'"])

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

    caps = caps_lock
    esc = escape
    ins = insert
    windows = Key(alias_for=[left_windows_key, right_windows_key])

    lshift = left_shift
    rshift = right_shift
    shift = Key(16, "VK_SHIFT", alias_for=[left_shift, right_shift])
    lcontrol = left_control
    lctrl = left_control
    rcontrol = right_control
    rctrl = right_control
    ctrl = Key(17, "VK_CONTROL", alias_for=[left_control, right_control])
    lalt = left_alt
    ralt = right_alt
    alt = Key(18, "VK_MENU", alias_for=[left_alt, right_alt])

    dash = minus
    hyphen = minus
    dot = period


