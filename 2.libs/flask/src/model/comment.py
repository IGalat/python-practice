from dataclasses import dataclass

from model.article import Article


@dataclass
class Comment:
    id: int
    article: Article
    author: str
    text: str
