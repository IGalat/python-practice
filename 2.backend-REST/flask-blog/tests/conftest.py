import os
import sys

import pytest
from flask_app import create_app

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")


@pytest.fixture
def is_debug() -> bool:
    return hasattr(sys, "gettrace") and (sys.gettrace() is not None)


# These 3 fixtures are not actually used, I just use blueprint fixtures
@pytest.fixture
def flask_app():
    flask_app = create_app()
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield flask_app

    # clean up / reset resources here


@pytest.fixture
def flask_client(flask_app):
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture
def runner(flask_app):
    return flask_app.test_cli_runner()
