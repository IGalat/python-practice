from abc import ABC, abstractmethod

from tap import Tap
from util.key_state import EmulatedKeypressManager, HotkeyMatcher


class BaseAdapter(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        """And clear resources, this is terminal"""
        pass

    @abstractmethod
    def press_key(self) -> None:
        pass

    @abstractmethod
    def release_key(self) -> None:
        pass

    @staticmethod
    def on_press(vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button press
        :param vk: virtual code of button pressed
        :return If True, press should be propagated
        If False, should be suppressed
        """
        if not EmulatedKeypressManager.was_pressed_real(vk):
            return True
        # todo record keypress, for hotstring
        potential_taps: list[Tap] = HotkeyMatcher.hotkeys_with_trigger(vk)
        if not potential_taps:
            return True

    @staticmethod
    def on_release(vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button release
        :param vk: virtual code of button released
        :return If True, key release should be propagated
        If False, should be suppressed
        """
        return True
