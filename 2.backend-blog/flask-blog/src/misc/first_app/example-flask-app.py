from flask import Flask, url_for, redirect, abort, request
from werkzeug.wrappers.response import Response

# launch from .sh

app = Flask(__name__)


@app.get("/")
def index() -> str:
    return "index"


@app.get("/login")
def login() -> str:
    return "login"


@app.get("/user/<username>")
def profile(username: str) -> str:
    return f"{username}'s profile"


@app.route("/redirect_me")
def redirect_me() -> Response:
    return redirect(url_for("abort401"))


@app.route("/abort401")
def abort401() -> None:
    abort(401)  # responds with html page, unacceptable for backend


@app.route("/login_request_obj_showcase", methods=["POST", "GET"])
def login_request_obj_showcase() -> tuple[str, int]:
    error = "Should make a POST request to this endpoint"
    if request.method == "POST":
        if (  # this is crap, has to be an easier way to null guard
            hasattr(request, "form")
            and hasattr(request.form, "username")
            and request.form["username"] == request.form["password"]
        ):
            return request.form["username"], 200
        else:
            error = "Invalid username/password"
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return error, 401
