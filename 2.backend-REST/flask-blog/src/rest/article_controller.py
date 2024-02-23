# import json
from dataclasses import asdict

from flask import Blueprint
from flask import request
from flask import Response
from flask.typing import ResponseReturnValue
from model.article import Article
from service import article_service

# from http import HTTPStatus

article_controller = Blueprint("article_routes", __name__, template_folder="/templates")


@article_controller.get("/")
def get_all() -> ResponseReturnValue:
    # Flask auto-converts lists and dicts to json in response data
    # But not recursively, and not for dataclasses or others

    # Implicit 200 OK here
    return [asdict(a) for a in article_service.get_all()]
    # Shorthand for:
    # return Response(status=HTTPStatus.OK
    #                 , response=[json.dumps(asdict(a)) for a in article_service.get_all()]
    #                 , mimetype='application/json')


@article_controller.get("/<int:id>")
def get_one(id: int) -> ResponseReturnValue:
    return asdict(article_service.get_one(id))


@article_controller.get("/name/<string:name>")
def get_by_name(name: str) -> ResponseReturnValue:
    return asdict(article_service.get_by_name(name))


@article_controller.get("/stats")
def get_stats() -> ResponseReturnValue:
    return asdict(article_service.get_stats())


@article_controller.post("/")
def add_one() -> ResponseReturnValue:
    article: Article = request.get_json()
    article_service.add_one(article)
    return Response(status=202)


@article_controller.patch("/<int:id>")
def update_one(id: int) -> ResponseReturnValue:
    article: Article = request.get_json()
    article.id = id
    article_service.update_one(article)
    return Response(status=202)


@article_controller.delete("/<int:id>")
def delete_one(id: int) -> ResponseReturnValue:
    article_service.delete_one(id)
    return Response(status=202)
