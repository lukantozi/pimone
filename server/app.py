from flask import Flask, jsonify, request
from store import metric_store
import requests


app = Flask(__name__)


@app.route("/metrics", methods=["POST"])
def metrics():
    if request.method == "POST":
        data = request.json
        metric_store.store(data)
        return "Success", 200
    else:
        return "Method Not Allowed", 405

@app.route("/status", methods=["GET"])
def status():
    if request.method == "GET":
        return metric_store.get
    else:
        return "Method Not Allowed", 405


if __name__ == "__main__":
    app.run(debug=True)
