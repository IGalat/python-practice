from dataclasses import asdict

from flask import Blueprint
from flask import request
from flask import Response
from flask.typing import ResponseReturnValue
from model.comment import Comment
from service import comment_service

comment_controller = Blueprint("comment_routes", __name__, template_folder="/templates")


@comment_controller.get("/")
def get_all() -> ResponseReturnValue:
    return [asdict(a) for a in comment_service.get_all()]


@comment_controller.get("/<int:id>")
def get_one(id: int) -> ResponseReturnValue:
    return asdict(comment_service.get_one(id))


@comment_controller.get("/articles/<int:article_id>")
def get_by_article_id(article_id: int) -> ResponseReturnValue:
    return [asdict(a) for a in comment_service.get_by_article_id(article_id)]


@comment_controller.get("/authors/<string:author>")
def get_by_author(author: str) -> ResponseReturnValue:
    return [asdict(a) for a in comment_service.get_by_author(author)]


@comment_controller.post("/")
def add_one() -> ResponseReturnValue:
    comment: Comment = request.get_json()
    comment_service.add_one(comment)
    return Response(status=202)


@comment_controller.patch("/<int:id>")
def update_one(id: int) -> ResponseReturnValue:
    comment: Comment = request.get_json()
    comment.id = id
    comment_service.update_one(comment)
    return Response(status=202)


@comment_controller.delete("/<int:id>")
def delete_one(id: int) -> ResponseReturnValue:
    comment_service.delete_one(id)
    return Response(status=202)
