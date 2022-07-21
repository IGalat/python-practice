import os
import signal
import subprocess
import sys

from config import Config


class TapControl:  # todo
    @staticmethod
    def restart_script() -> None:
        print("Restarting script...")
        sys.stdout.flush()
        subprocess.Popen([sys.executable] + sys.argv, creationflags=subprocess.DETACHED_PROCESS)
        os.kill(os.getpid(), signal.SIGINT)

    @staticmethod
    def terminate_script() -> None:
        print("Terminating script...")
        Config.adapter.stop()
        os.kill(os.getpid(), signal.SIGINT)
