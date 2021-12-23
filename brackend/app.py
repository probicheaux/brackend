import json
import logging
import math
from datetime import datetime
from os.path import dirname, join

from flask import Flask, jsonify, request
from flask_cors import CORS

from brackend.tasks.auth import get_password_and_salt
from brackend.tasks.tasks import (
    get_tournament_ids,
    get_user_ids,
    login_user,
    save_new_tournament,
    save_new_user_email,
)
from brackend.util import BrackendException

# App Blueprints: Blueprint for each resource
from brackend.endpoints.tournaments.tournaments import tournament_bp

api_prefix_v1 = "/api/v1"
def register_blueprints(app):
    """
        Register all blueprints for the app
    """
    app.register_blueprint(tournament_bp, url_prefix=api_prefix_v1)

app = Flask(__name__)
path = dirname(__file__)
CORS(app)
register_blueprints(app)
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Brackets are arranged in a certain way, and we use this function to return a list of numbers that show where each value should
# be rearranged to.
def generateSeedPos(n):
    r = list(range(n))
    s = 1
    while s < n // 2:
        tmp = r
        r = []
        while len(tmp) > 0:
            d = tmp[:s]
            del tmp[:s]
            e = tmp[len(tmp) - s :]
            del tmp[len(tmp) - s :]
            r = r + d
            r = r + e
        s *= 2
    return r


def mock_rounds():
    with open(join(path, "mock_rounds.json")) as file:
        return json.load(file)


@app.route("/api/hello/", methods=["GET"])
def hello():
    return jsonify(success=True)


@app.route("/api/user/register-from-email/", methods=["POST"])
def register_user():
    response_json = request.get_json()
    username = response_json.get("username")
    password = response_json.get("password")
    email = response_json.get("email")
    password = get_password_and_salt(password)
    save_new_user_email.send(username, password, email)
    return jsonify(success=True)


@app.route("/api/user/login/", methods=["POST"])
def login():
    response_json = request.get_json()
    username = response_json.get("username")
    password = response_json.get("password")
    try:
        jwt = login_user(username, password)
        return jsonify(success=True, token=jwt)
    except BrackendException as error:
        app.log_exception(error)
        return jsonify(success=False, token=None)


@app.route("/api/user/logout/", methods=["POST"])
def logout():
    response_json = request.get_json()
    username = response_json.get("username")
    password = response_json.get("password")
    app.logger.info("Got POST at /api/user/logout/")
    return jsonify(token="truthy token: u: " + username + " p: " + password)


@app.route("/api/tournament/register/", methods=["POST"])
def register_tournament():
    response_json = request.get_json()
    name = response_json.get("name")
    save_new_tournament.send(name)
    return jsonify(success=True)


@app.route("/api/user/list/", methods=["GET"])
def get_users():
    return jsonify(get_user_ids())


@app.route("/api/tournament/list/", methods=["GET"])
def get_tournaments():
    return jsonify(get_tournament_ids())


@app.route("/api/tournament/", methods=["POST"])
def tournament():
    request_json = request.get_json()
    tourney_id = request_json.get("tourney_id")
    app.logger.info(f"Got post at /api/tournament/")
    app.logger.info(f"tourney_id: {tourney_id}")

    return jsonify(rounds=mock_rounds())


@app.route("/api/tournament/makeBracketFromEntrants/", methods=["POST"])
def makeBracketFromEntrants():
    request_json = request.get_json()
    app.logger.info(f"Got post at /api/makeBracketFromEntrants/")
    players = request_json.get("players")
    base_num = 2 ** math.floor(math.log(len(players), 2))
    seg = base_num - (len(players) - base_num)
    round_two_players = players[:seg]
    round_one_players = players[seg:]
    date = request_json.get("date")
    if date == None:
        date = datetime.today().strftime("%Y-%m-%d")

    matches = {
        "winners": [
            {"title": "Winner's Round 1", "seeds": []},
            {"title": "Winner's Round 2", "seeds": []},
        ],
        "losers": [],
    }

    round_one = [
        {
            "id": i,
            "losers": False,
            "date": date,
            "teams": [{"name": "", "game": -1}, {"name": "", "game": -1}],
        }
        for i in range(base_num)
    ]
    pos = generateSeedPos(base_num)
    b = 0
    while len(round_one_players) > 0:
        place = pos.index(b)
        round_one[place]["teams"][0]["name"] = round_one_players.pop(
            len(round_one_players) // 2 - 1
        )
        round_one[place]["teams"][1]["name"] = round_one_players.pop(len(round_one_players) // 2)
        b += 1
    matches["winners"][0]["seeds"] = round_one

    round_two = [
        {
            "id": i,
            "losers": False,
            "date": date,
            "teams": [{"name": "", "game": -1}, {"name": "", "game": -1}],
        }
        for i in range(base_num // 2)
    ]
    pos2 = generateSeedPos(base_num)
    for p in range(len(round_two_players)):
        place2 = pos2.index(p)
        round_two[place2 // 2]["teams"][place2 % 2]["name"] = round_two_players[p]
    matches["winners"][1]["seeds"] = round_two

    return jsonify(rounds=matches)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
