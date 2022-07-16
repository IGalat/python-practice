from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        """And clear resources, this is terminal"""
        pass

    def on_press(self, vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button press
        :param vk: virtual code of button pressed
        :return If True, press should be propagated
        If False, should be suppressed
        """

        return True

    def on_release(self, vk: int) -> bool:
        """
        Adapters call this on mouse/keyboard button release
        :param vk: virtual code of button released
        :return If True, key release should be propagated
        If False, should be suppressed
        """
        return True
