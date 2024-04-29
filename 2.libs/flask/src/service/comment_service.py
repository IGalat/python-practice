from model.comment import Comment


def get_all() -> list[Comment]:
    pass


def get_one(id: int) -> Comment:
    pass


def get_by_article_id(article_id: int) -> list[Comment]:
    pass


def get_by_author(author: str) -> list[Comment]:
    pass


def add_one(comment: Comment) -> bool:
    pass


def update_one(comment: Comment) -> bool:
    pass


def delete_one(id: int) -> bool:
    pass
