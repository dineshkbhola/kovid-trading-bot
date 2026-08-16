from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "dashboard/live_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "nifty": 0,
            "ce": 0,
            "pe": 0,
            "signal": "WAIT"
        }

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "nifty": 0,
            "ce": 0,
            "pe": 0,
            "signal": "ERROR"
        }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data")
def data():
    return jsonify(load_data())


# 👇 THIS IS CRITICAL
def run_dashboard():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)