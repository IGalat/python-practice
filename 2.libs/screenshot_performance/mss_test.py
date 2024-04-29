import time

import mss.tools


def screenshot_to_file(filename: str) -> None:
    with mss.mss() as sct:
        sct.shot(output=filename + ".png")
        sct.shot()


def screen_bbox(filename: str) -> None:
    with mss.mss() as sct:
        bbox = (0, -1080, 1919, 0)
        im = sct.grab(bbox)
        mss.tools.to_png(
            im.rgb,
            im.size,
            output=rf"{filename}-(BBOX_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}).png",
        )


def perf_test() -> None:
    start = time.perf_counter()
    bbox = (0, -1080, 1919, 1079)
    with mss.mss() as sct:
        for _ in range(100):
            im = sct.grab(bbox)
            mss.tools.to_png(im.rgb, im.size, output=rf"mss.png")
    print(f"Performance: 100 screenshots in {time.perf_counter()-start:.3f}s")


def main() -> None:
    # screenshot_to_file("mss")
    # screen_bbox("C:\_my\img")  # abs path
    # screen_bbox("img")  # relative

    perf_test()


if __name__ == "__main__":
    main()
