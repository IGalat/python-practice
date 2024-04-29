from dataclasses import dataclass
from dataclasses import field

from typing_extensions import Literal
from typing_extensions import Self

PATH_TO_FICS = r"C:\_my\my\tng-private\fics"
DELIMITER = "::"


@dataclass
class Link:
    name: str
    hyperlink: str


@dataclass
class Folder:
    status: Literal["SAME", "OLD", "NEW"] = "NEW"
    folders: dict[str, Self] = field(default_factory=lambda: {})
    links: list[Link] = field(default_factory=lambda: [])

    def get_linknames(self, path_parts: list[str] | None = None) -> list[list[str]]:
        path_parts = path_parts or []
        result = []

        if self.folders:
            for name, folder in self.folders.items():
                result.extend(folder.get_linknames(path_parts + [name]))

        if self.links:
            result.extend([path_parts + [link.name] for link in self.links])
        return result
