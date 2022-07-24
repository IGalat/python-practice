from abc import ABC, abstractmethod

from key import Keys
from tap import Tap
from util.action_runner import ActionRunner
from util.key_state import KeypressManager, HotkeyMatcher


class BaseAdapter(ABC):  # todo move all logic from here, on_press substitute f
    """
    To use an adapter that implements this, set it as value of Config.adapter
    """

    _NEVER_PRESSED_OR_TOGGLED = (Keys.scroll_wheel_up.vk_code, Keys.scroll_wheel_down.vk_code)

    @classmethod
    @abstractmethod
    def start(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def stop(cls) -> None:
        """And clear resources, this is terminal"""
        pass

    @classmethod
    @abstractmethod
    def press_key(cls, vk_code: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def release_key(cls, vk_code: int) -> None:
        pass

    @classmethod
    def on_press(cls, vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button press
        :param vk: virtual code of button pressed
        :return If True, press should be propagated
        If False, should be suppressed
        """
        print(f"Pressed vk: {vk}, all_keys_pressed: {KeypressManager.keys_pressed()}")
        if not KeypressManager.was_pressed_real(vk):
            return True
        # todo record keypress, for hotstring
        potential_taps: list[Tap] = HotkeyMatcher.active_hotkeys_with_trigger(vk)
        if not potential_taps:
            return True
        vk_pressed: set[int] = KeypressManager.keys_pressed()
        try:
            tap_selected = next(tap for tap in potential_taps if BaseAdapter.all_keys_pressed(tap, vk_pressed))
            if not tap_selected.action:
                return True  # action is "None" so pass through
        except StopIteration:  # no match
            return True
        ActionRunner.run(tap_selected.action)
        return not tap_selected.suppress_trigger_key_on_action

    @staticmethod
    def all_keys_pressed(tap: Tap, vk_pressed: set[int]) -> bool:
        for key in tap.additional_keys:
            if not any(vk in vk_pressed for vk in key.all_vk_codes):
                return False
        if tap.no_additional_keys:
            if len(vk_pressed) > (len(tap.additional_keys) + 1):  # todo check instead every key pressed
                return False
        return True

    @classmethod
    def on_release(cls, vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button release
        :param vk: virtual code of button released
        :return If True, key release should be propagated
        If False, should be suppressed
        """
        print(f"Released vk: {vk}, all_keys_pressed: {KeypressManager.keys_pressed()}")
        if not KeypressManager.was_released_real(vk):
            return True
        return True

    @classmethod
    def pressed(cls, vk_code: int) -> bool:
        if vk_code in cls._NEVER_PRESSED_OR_TOGGLED:
            return False
        else:
            return cls._pressed(vk_code)

    @classmethod
    @abstractmethod
    def _pressed(cls, vk_code: int) -> bool:
        pass

    @classmethod
    def toggled(cls, vk_code: int) -> bool:
        if vk_code in cls._NEVER_PRESSED_OR_TOGGLED:
            return False
        else:
            return cls._toggled(vk_code)

    @classmethod
    @abstractmethod
    def _toggled(cls, vk_code: int) -> bool:
        pass

    @classmethod
    def press_mouse_button(cls, vk_code: int) -> None:
        if vk_code == Keys.scroll_wheel_up.vk_code:
            cls.move_mousewheel(1)
        elif vk_code == Keys.scroll_wheel_down.vk_code:
            cls.move_mousewheel(-1)
        else:
            cls._press_mouse_button(vk_code)

    @classmethod
    @abstractmethod
    def _press_mouse_button(cls, vk_code: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def release_mouse_button(cls, vk_code: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def move_mousewheel(cls, times: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def move_mouse(cls, dx: int, dy: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def set_mouse_pos(cls, x: int, y: int) -> None:
        pass

    @classmethod
    @abstractmethod
    def get_mouse_pos(cls) -> tuple[int, int]:
        pass
