import subprocess
import sys
from typing import Optional

from tap_group import TapGroup


class TapControl:  # todo
    @staticmethod
    def restart_script() -> None:
        pass

    @staticmethod
    def terminate_script() -> None:
        pass

    @staticmethod
    def reload_script() -> None:
        sys.stdout.flush()
        subprocess.Popen([sys.executable] + sys.argv, creationflags=subprocess.DETACHED_PROCESS)
        sys.exit()

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
