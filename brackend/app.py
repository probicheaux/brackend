import json
import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from os.path import dirname, join

app = Flask(__name__)
path = dirname(__file__)
CORS(app)
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def mock_rounds():
    with open(join(path, "mock_rounds.json")) as file:
        return json.load(file)


@app.route("/api/hello/", methods=["GET"])
def hello():
    return jsonify(token="ya mum")


@app.route("/api/login/", methods=["POST"])
def login():
    json = request.get_json()
    username = json.get("username")
    password = json.get("password")
    app.logger.info("Got post at /api/login/")
    app.logger.info(f"Username: {username}")
    app.logger.info(f"Password: {password}")
    return jsonify(token="truthy token: u: " + username + " p: " + password)


@app.route("/api/tournament/", methods=["POST"])
def tournament():
    json = request.get_json()
    tourney_id = json.get("tourney_id")
    app.logger.info(f"Got post at /apit/tournament/")
    app.logger.info(f"tourney_id: {tourney_id}")

    return jsonify(rounds=mock_rounds())


if __name__ == "__main__":
    app.run(host="0.0.0.0")
