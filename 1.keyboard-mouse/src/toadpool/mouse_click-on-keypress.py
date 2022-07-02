import keyboard
import mouse

# works reliably: with any mod key, and always detects

counter: int = 1


def print_and_incr() -> None:
    global counter
    print(f"{counter} times RMB clicked!")
    counter += 1


mouse.on_right_click(print_and_incr)
keyboard.wait("q")
