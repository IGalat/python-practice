import cv2


def get_coords_in_image(name_outer: str, name_inner: str) -> tuple[int, int] | None:
    """Detects the closest thing, even when image is not there."""
    outer = cv2.imread(name_outer)
    inner = cv2.imread(name_inner)

    result = cv2.matchTemplate(outer, inner, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, max_val, min_loc, max_loc)

    return max_loc if max_val > 0.8 else None


def main() -> None:
    print(get_coords_in_image("Rainforest.png", "Yellowing-leaf.png"))
    print(get_coords_in_image("Rainforest.png", "Filtered-Yellowing-leaf.png"))
    print(get_coords_in_image("Yellowing-leaf.png", "Filtered-Yellowing-leaf.png"))
    print(get_coords_in_image("Rainforest.png", "not-in-pic.png"))
    print(get_coords_in_image("Rainforest.png", "another-not-in.png"))


if __name__ == "__main__":
    main()
