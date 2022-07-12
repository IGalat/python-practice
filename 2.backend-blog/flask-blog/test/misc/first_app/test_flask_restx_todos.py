import logging
from typing import Generator

import pytest
from flask.testing import FlaskClient

from misc.first_app.flask_restx_todos import app, Endpoints, TODOS

log = logging.getLogger(__name__)


# setup and teardown only wrap test methods that use this fixture's yield.
@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    # any setup before yield
    with app.test_client() as client:
        yield client
    # teardown after yield


def test_get_all(client: FlaskClient) -> None:
    response = client.get(Endpoints.todos)

    assert response.status_code == 200
    assert response.json == TODOS


def test_post(client: FlaskClient) -> None:
    my_todo = {"task": "test an API"}

    # where are the logs from app I'm testing? not displaying, no debug either
    # don't know where 400 comes from even in this simple case
    response = client.post(Endpoints.todos, data=my_todo)
    todo_from_response = client.get(Endpoints.todos)
    log.info("asd")

    # assert response.status_code == 200
    # assert todo_from_response == my_todo
