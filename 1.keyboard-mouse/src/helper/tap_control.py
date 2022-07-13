from typing import Optional

from tap_group import TapGroup


class TapControl:
    @staticmethod
    def restart_script() -> None:
        pass

    @staticmethod
    def terminate_script() -> None:
        pass

    @staticmethod
    def suspend(tap_group: Optional[TapGroup]) -> None:
        """If no tap_group, suspends hotkeys globally, except control group"""
        pass

    @staticmethod
    def unsuspend(tap_group: Optional[TapGroup]) -> None:
        """If no tap_group, un-suspends hotkeys globally, except control group"""
        pass

    @staticmethod
    def toggle_suspend(tap_group: Optional[TapGroup]) -> None:
        """If no tap_group, toggles hotkeys globally, except control group"""
        pass
