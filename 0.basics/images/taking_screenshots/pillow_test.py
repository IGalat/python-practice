import time

import PIL.ImageGrab


def screenshot_to_file(filename: str) -> None:
    sct = PIL.ImageGrab.grab()
    with open(filename + ".png", "wb") as f:
        sct.save(f, "PNG")


def screen_bbox(filename: str, bbox: tuple[int, int, int, int]) -> None:
    sct = PIL.ImageGrab.grab(bbox=bbox, all_screens=True)
    with open(filename + ".png", "wb") as f:
        sct.save(f, "PNG")


def perf_test() -> None:
    start = time.perf_counter()
    for _ in range(100):
        sct = PIL.ImageGrab.grab(all_screens=True)
        with open("pil.png", "wb") as f:
            sct.save(f, "PNG")
    print(f"Performance: 100 screenshots in {time.perf_counter()-start:.3f}s")


def main() -> None:
    # screenshot_to_file("pillow_screenshot")

    # screen_bbox("img", (200, -900, 1600, -200))  # negative coords require all_screens

    # screen_bbox("img", (200, 100, 1600, 1000))
    # screen_bbox("img", (0, -1080, 1919, 0))

    perf_test()


if __name__ == "__main__":
    main()
