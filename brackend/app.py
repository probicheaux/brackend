import json
import logging
import math
from datetime import datetime
from os.path import dirname, join

from flask import Flask, jsonify, request
from flask_cors import CORS

# App Blueprints: Blueprint for each resource
from brackend.endpoints.tournaments import tournament_bp
from brackend.endpoints.users import users_bp
from brackend.endpoints.brackets import brackets_bp

api_prefix_v1 = "/api/v1"


def register_blueprints(app):
    """Register all blueprints for the app."""
    app.register_blueprint(tournament_bp, url_prefix=api_prefix_v1)
    app.register_blueprint(users_bp, url_prefix=api_prefix_v1)
    app.register_blueprint(brackets_bp, url_prefix=api_prefix_v1)


app = Flask(__name__)
path = dirname(__file__)
CORS(app)
register_blueprints(app)
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def mock_rounds():
    with open(join(path, "mock_rounds.json")) as file:
        return json.load(file)


@app.route("/api/hello/", methods=["GET"])
def hello():
    return jsonify(success=True)


@app.errorhandler(404)
def route_not_found(e):
    return jsonify({"error": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0")
