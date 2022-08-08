from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any
from typing import Optional


@dataclass
class Window:
    handle: Any
    pid: Optional[int]
    exec: Optional[str]
    title: Optional[str]


class WindowAdapterBase(ABC):
    """Only operates on visible windows with window text. May change"""

    @classmethod
    @abstractmethod
    def start(cls) -> None:
        pass

    @classmethod
    @abstractmethod
    def stop(cls) -> None:
        """And clear resources, this is terminal"""
        pass

    @classmethod
    @abstractmethod
    def get_open(
        cls,
        exec_or_title: Optional[str] = None,
        *,
        handle: Any = None,
        pid: Optional[int] = None,
        exec: Optional[str] = None,
        title: Optional[str] = None
    ) -> list[Window]:
        """
        :return: List of open windows, containing specified exec name and title
        With no inputs returns list of all open windows
        """
        pass

    @classmethod
    @abstractmethod
    def get_fore(
        cls,
        exec_or_title: Optional[str] = None,
        *,
        handle: Any = None,
        pid: Optional[int] = None,
        exec: Optional[str] = None,
        title: Optional[str] = None
    ) -> Optional[Window]:
        """
        :return: With no inputs returns current foreground window
        With inputs only returns if it matches, else None
        Can be used like this:
        # if adapter.get_fore(name = "notepad++")
        #     do my stuff
        """
        pass

    @classmethod
    @abstractmethod
    def set_fore(
        cls,
        exec_or_title: Optional[str] = None,
        *,
        handle: Any = None,
        pid: Optional[int] = None,
        exec: Optional[str] = None,
        title: Optional[str] = None
    ) -> bool:
        pass
