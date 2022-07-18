from abc import ABC, abstractmethod
from typing import Callable, Optional

from tap import Tap
from util.controller import ActionRunner
from util.key_state import KeypressManager, HotkeyMatcher


class BaseAdapter(ABC):  # todo move all logic from here, on_press substitute f
    """
    To use an adapter that implements this, set it as value of Config.adapter
    """

    @abstractmethod
    @classmethod
    def start(cls) -> None:
        pass

    @abstractmethod
    @classmethod
    def stop(cls) -> None:
        """And clear resources, this is terminal"""
        pass

    @abstractmethod
    @classmethod
    def press_key(cls) -> None:
        pass

    @abstractmethod
    @classmethod
    def release_key(cls) -> None:
        pass

    @classmethod
    def on_press(cls, vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button press
        :param vk: virtual code of button pressed
        :return If True, press should be propagated
        If False, should be suppressed
        """
        if not KeypressManager.was_pressed_real(vk):
            return True
        # todo record keypress, for hotstring
        potential_taps: list[Tap] = HotkeyMatcher.active_hotkeys_with_trigger(vk)
        if not potential_taps:
            return True
        vk_pressed: set[int] = KeypressManager.keys_pressed
        try:
            action_selected = next(BaseAdapter.should_run(tap, vk_pressed) for tap in potential_taps)
            if not action_selected:
                return True  # found "None" so pass through
        except StopIteration:  # no match
            return True
        ActionRunner.run(action_selected)
        return False

    @staticmethod
    def should_run(potential_taps: Tap, vk_pressed: set[int]) -> Optional[Callable]:
        pass

    @classmethod
    def on_release(cls, vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button release
        :param vk: virtual code of button released
        :return If True, key release should be propagated
        If False, should be suppressed
        """
        return True
