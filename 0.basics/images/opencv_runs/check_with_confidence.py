import cv2
import numpy
import PIL.Image
from numpy import ndarray

outer = "img-mss.png"
inner = [
    "img-pil.png",
]


def compare_confidence(outer_arr: ndarray, inner_arr: ndarray) -> float:
    comparison = cv2.matchTemplate(outer_arr, inner_arr, cv2.TM_CCORR_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(comparison)
    return max_val


def main() -> None:
    convert = lambda image: numpy.asarray(PIL.Image.open(image).convert("RGB"))
    for pic in inner:
        cut_pic = convert(pic)[:, 6:-6]
        print(
            f"{pic}, confidence: {compare_confidence(convert(outer), convert(pic)):.2f}, "
            f"cut={compare_confidence(convert(outer), cut_pic):.2f}"
        )


if __name__ == "__main__":
    main()
