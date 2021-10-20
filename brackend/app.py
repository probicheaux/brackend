from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hell():
    return jsonify(token="ya mum")

@app.route("/api/hello/", methods=["GET"])
def hello():
    return jsonify(token="ya mum")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
