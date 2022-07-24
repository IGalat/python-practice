from dataclasses import dataclass
from threading import Lock
from typing import Optional, Final

from typing_extensions import Self

_SUSPEND_AUTO_REASON: Final[str] = "_auto"


@dataclass(repr=False)
class Suspendable:
    _suspended: set[str]

    def __repr__(self) -> str:
        if self._suspended:
            return f"suspended={self._suspended}"
        else:
            return ""

    def suspend(self, source: Optional[str] = None) -> bool:
        src = source or _SUSPEND_AUTO_REASON
        if src in self._suspended:
            return False
        else:
            self._suspended.add(source or _SUSPEND_AUTO_REASON)
            return True

    def unsuspend(self, source: Optional[str] = None) -> bool:
        if not hasattr(self, "_suspended"):
            self._suspended = set()
            return True
        try:
            self._suspended.remove(source or _SUSPEND_AUTO_REASON)
            return True
        except KeyError:
            return False

    def toggle_suspend(self, source: Optional[str] = None) -> None:
        if not self.unsuspend(source):
            self.suspend(source)

    def suspended(self) -> set[str]:
        return self._suspended is None or len(self._suspended) > 0


class SingletonMeta(type):
    _instances: dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs) -> Self:  # type:ignore
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
