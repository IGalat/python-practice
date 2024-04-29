from dataclasses import dataclass


@dataclass
class Article:
    id: int
    name: str
    text: str


@dataclass
class ArticleStats:
    id: int
    name: str
