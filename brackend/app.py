from flask import Flask, jsonify, request

import logging
logger = logging.Logger(__name__)
app = Flask(__name__)

@app.route("/api/hello/", methods=["GET"])
def hello():
    return jsonify(token="ya mum")

@app.route("/api/login/", methods=["POST"])
def login():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')
    logger.info("GOT POST")
    logger.info(f"{username}=")
    logger.info(f"{password}=")
    return jsonify(token='this is a token from the real api, '+username+password)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
