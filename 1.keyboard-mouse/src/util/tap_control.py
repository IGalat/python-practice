import subprocess
import sys


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
