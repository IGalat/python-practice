"""press all chars, wrap in quotes"""
import time

import winput
from key import Keys

symbols = [
    Keys.backtick,
    Keys.one,
    Keys.two,
    Keys.three,
    Keys.four,
    Keys.five,
    Keys.six,
    Keys.seven,
    Keys.eight,
    Keys.nine,
    Keys.zero,
    Keys.minus,
    Keys.equals,
    Keys.q,
    Keys.w,
    Keys.e,
    Keys.r,
    Keys.t,
    Keys.y,
    Keys.u,
    Keys.i,
    Keys.o,
    Keys.p,
    Keys.square_bracket_open,
    Keys.square_bracket_close,
    Keys.backslash,
    Keys.a,
    Keys.s,
    Keys.d,
    Keys.f,
    Keys.g,
    Keys.h,
    Keys.j,
    Keys.k,
    Keys.l,
    Keys.semicolon,
    Keys.quote,
    Keys.z,
    Keys.x,
    Keys.c,
    Keys.v,
    Keys.b,
    Keys.n,
    Keys.m,
    Keys.comma,
    Keys.period,
    Keys.slash,
]


def main() -> None:
    for key in symbols:
        winput.click_key(key.vk_code)
    winput.press_key(Keys.left_shift.vk_code)
    time.sleep(0.001)
    for key in symbols:
        winput.click_key(key.vk_code)
    winput.release_key(Keys.left_shift.vk_code)
    winput.click_key(Keys.delete.vk_code)


if __name__ == "__main__":
    main()
