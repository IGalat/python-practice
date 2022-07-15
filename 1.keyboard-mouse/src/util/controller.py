import subprocess
import sys


def reload_script() -> None:
    sys.stdout.flush()
    subprocess.Popen([sys.executable] + sys.argv, creationflags=subprocess.DETACHED_PROCESS)
    sys.exit()
