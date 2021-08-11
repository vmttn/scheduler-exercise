from http import HTTPStatus
from flask import Flask, request

app = Flask(__name__)


@app.route('/<string:username>', methods=["GET"])
def hello(username: str):
    return f'Hello, {username}!', HTTPStatus.OK


@app.route('/', methods=["GET", "POST"])
def hello_world():
    payload = request.get_json(force=True, silent=True)
    if payload is not None and "name" in payload:
        return hello(payload["name"])

    return hello("World")


if __name__ == '__main__':
    # noinspection FlaskDebugMode
    app.run(debug=True)
