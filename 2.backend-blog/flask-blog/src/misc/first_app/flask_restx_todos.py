from enum import Enum

from flask import Flask
from flask_restx import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)


class Endpoints(str, Enum):
    todos: str = "todos"


TODOS = {
    "todo1": {"task": "build an API"},
    "todo2": {"task": "?????"},
    "todo3": {"task": "profit!"},
}


def abort_if_todo_doesnt_exist(todo_id: str) -> None:
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument("task")


class Todo(Resource):
    @staticmethod
    def get(todo_id: str) -> tuple[dict[str, str], int]:
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id], 200

    @staticmethod
    def delete(todo_id: str) -> tuple[str, int]:
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return "", 204

    @staticmethod
    def put(todo_id: str) -> tuple[dict[str, str], int]:
        args = parser.parse_args()
        task = {"task": args["task"]}
        TODOS[todo_id] = task
        return task, 201


class TodoList(Resource):
    @staticmethod
    def get() -> tuple[dict[str, dict[str, str]], int]:
        return TODOS, 200

    @staticmethod
    def post() -> tuple[dict[str, str], int]:
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip("todo")) + 1
        todo_id = "todo%i" % todo_id
        TODOS[todo_id] = {"task": args["task"]}
        return TODOS[todo_id], 201


api.add_resource(TodoList, Endpoints.todos)
api.add_resource(Todo, Endpoints.todos + "/<todo_id>")

if __name__ == "__main__":
    app.run(debug=True)
