from flask import Flask
from rest.controllers import rest_controllers


# run command, form this folder, with active venv:
# flask --app flask_app.py run
# or with debugger, can interfere with IDEA debugger, catches exceptions before IDEA can
# flask --app flask_app.py run --debug


def create_app() -> Flask:
    app = Flask(__name__)

    # https://flask.palletsprojects.com/en/latest/blueprints/
    # Blueprints are a way to loosely couple resources
    for prefix, controller in rest_controllers.items():
        app.register_blueprint(controller, url_prefix=prefix)

    return app


create_app()
