import json
import logging
from os.path import dirname, join

from flask import Flask, jsonify, request
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
path = dirname(__file__)
CORS(app)
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

# Brackets are arranged in a certain way, and we use this function to return a list of numbers that show where each value should
# be rearranged to.
def generateSeedPos(n):
    if n == 1:
        return [0]
    if n == 2:
        return [0,1]
    if n == 4:
        return [0,3,1,2]
    if n == 8:
        return [0,7,3,4,1,6,2,5]
    r = list(range(n))
    s = 1
    while s < n//2:
        tmp = r
        r = []
        while len(tmp) > 0:
            d = tmp[:s]
            del tmp[:s]
            e = tmp[len(tmp)-s:]
            del tmp[len(tmp)-s:]
            r = r+d
            r = r+e
        s *= 2
    return r

def mock_rounds():
    with open(join(path, "mock_rounds.json")) as file:
        return json.load(file)


@app.route("/api/hello/", methods=["GET"])
def hello():
    return jsonify(token="ya mum")


@app.route("/api/login/", methods=["POST"])
def login():
    response_json = request.get_json()
    username = response_json.get("username")
    password = response_json.get("password")
    app.logger.info("Got post at /api/login/")
    app.logger.info(f"Username: {username}")
    app.logger.info(f"Password: {password}")
    return jsonify(token="truthy token: u: " + username + " p: " + password)


@app.route("/api/tournament/", methods=["POST"])
def tournament():
    request_json = request.get_json()
    tourney_id = request_json.get("tourney_id")
    app.logger.info(f"Got post at /api/tournament/")
    app.logger.info(f"tourney_id: {tourney_id}")

    return jsonify(rounds=mock_rounds())

@app.route("/api/makeBracketFromEntrants/", methods=["POST"])
def makeBracketFromEntrants():
    request_json = request.get_json()
    players = request_json.get("players")
    baseNum = 1
    while baseNum * 2 <= len(players):
        baseNum = baseNum * 2
    date = request_json.get("date")
    if date == None:
        date = datetime.today().strftime('%Y-%m-%d')
    iDee = 0
    matches = {"winners": [{"title": "Winner's Round 1", "seeds": []}, {"title": "Winner's Round 2", "seeds": []}], "losers": []}
    roundOne = [{"id": -1, "losers": False, "date": date, "teams": []} for i in range(baseNum//2)]
    matches["winners"][0]["seeds"] = roundOne
    return jsonify(matches)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
