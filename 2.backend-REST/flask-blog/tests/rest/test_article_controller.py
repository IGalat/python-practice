from typing import Any
from typing import Generator
from unittest.mock import Mock

import pytest
from flask import Flask
from flask.testing import FlaskClient
from model.article import Article
from rest.article_controller import article_controller


# Independent of global app, this is just for the blueprint
# As such, no /articles prefix in paths when testing
@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    flask_app = Flask(__name__)
    flask_app.register_blueprint(article_controller)
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


article_1 = Article(111, "1article name", "1article text lorem ipsum")
article_2 = Article(222, "2article name", "2article text lorem ipsum")
articles = [article_1, article_2]


def data_to_article(
    article_data: dict[Any, Any] | list[Any]
) -> Article | list[Article]:
    if isinstance(article_data, list):
        return [Article(**json_article) for json_article in article_data]
    else:
        return Article(**article_data)


def test_get_all__has_content(client: FlaskClient, mocker: Mock) -> None:
    mocker.patch(
        "rest.article_controller.article_service.get_all", return_value=articles
    )

    response = client.get("/")

    assert response.status_code == 200
    assert data_to_article(response.get_json()) == articles


def test_get_all__no_content(client: FlaskClient, mocker: Mock) -> None:
    mocker.patch("rest.article_controller.article_service.get_all", return_value=[])

    response = client.get("/")

    assert response.status_code == 200
    assert data_to_article(response.get_json()) == []


def test_get_one__happy_path(client: FlaskClient, mocker: Mock) -> None:
    mocker.patch(
        "rest.article_controller.article_service.get_one", return_value=article_2
    )

    response = client.get(f"/{article_2.id}")

    assert response.status_code == 200
    assert data_to_article(response.get_json()) == article_2


def test_get_one__not_found(client: FlaskClient, mocker: Mock) -> None:
    mocker.patch(
        "rest.article_controller.article_service.get_one",
        side_effect=Exception("Not found"),
    )

    # todo This should not raise, exception should be intercepted
    # https://flask.palletsprojects.com/en/latest/errorhandling/
    with pytest.raises(Exception) as e:
        response = client.get(f"/{article_2.id}")
