from flask import Flask, url_for, redirect, abort, request
from werkzeug.wrappers.response import Response

# launch from .sh in this folder

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
    print(request.data)
    if request.method == "POST":
        # assign and test for not none. won't use, might be smelly though convenient
        # assert (request_body := request.json)

        request_body = request.json
        assert request_body
        if request_body["username"] == request_body["password"]:
            return request_body["username"], 200
        else:
            error = "Invalid username/password"
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return error, 401
