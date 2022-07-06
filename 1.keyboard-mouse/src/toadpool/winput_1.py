import winput


# good base, reacts reliably. windows-only and no per-app though


def mouse_callback(event: winput.MouseEvent) -> None:
    if event.action == winput.WM_LBUTTONDOWN:
        print("Left mouse button press at {}".format(event.position))


def keyboard_callback(event: winput.KeyboardEvent) -> None:
    print(f'{event.action} {event.key}')
    if event.vkCode == winput.VK_ESCAPE:  # quit on pressing escape
        winput.stop()

    # OH SHIT loop!
    # if event.vkCode == winput.VK_J:
    #     winput.click_key(winput.VK_J)


print("Press escape to quit")

# hook input
winput.hook_mouse(mouse_callback)
winput.hook_keyboard(keyboard_callback)

# enter message loop
winput.wait_messages()

# remove input hook
winput.unhook_mouse()
winput.unhook_keyboard()
