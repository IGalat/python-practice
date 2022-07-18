from dataclasses import dataclass
from threading import Lock

from typing_extensions import Self


@dataclass
class Suspendable:
    _suspended: bool

    def suspend(self) -> None:
        self._suspended = True

    def unsuspend(self) -> None:
        self._suspended = False

    def toggle_suspend(self) -> None:
        self._suspended = not self._suspended

    def suspended(self) -> bool:
        return self._suspended


class SingletonMeta(type):
    _instances: dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs) -> Self:  # type:ignore # todo mypy
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
