from flask import Flask, request
from store import rolling


app = Flask(__name__)


@app.route("/metrics", methods=["POST"])
def metrics():
    if request.method == "POST":
        data = request.json
        rolling.store(data, 5)
        return "Success", 200
    else:
        return "Method Not Allowed", 405


@app.route("/status", methods=["GET"])
def status():
    if request.method == "GET":
        data = rolling.get
        print(len(data))
        return data
    else:
        return "Method Not Allowed", 405


@app.route("/status/avg-peak", methods=["GET"])
def average():
    if request.method == "GET":
        avg = rolling.average
        peak = rolling.peak
        return {
            "average": avg,
            "peak": peak,
        }
    else:
        return "Method Not Allowed", 405


if __name__ == "__main__":
    app.run(debug=True)
