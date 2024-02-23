from model.article import Article
from model.article import ArticleStats


def get_all() -> list[Article]:
    return [
        Article(111, "1 article name", "1article text lorem ipsum"),
        Article(222, "2 article name", "2article text lorem ipsum"),
    ]


def get_one(id: int) -> Article:
    pass


def get_by_name(name: str) -> Article:
    pass


def get_stats() -> ArticleStats:
    pass


def add_one(article: Article) -> bool:
    pass


def update_one(article: Article) -> bool:
    pass


def delete_one(id: int) -> bool:
    pass
