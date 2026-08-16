from flask import Flask, render_template, jsonify
import json
import os

# Correct template path
app = Flask(__name__, template_folder="templates")

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# FIXED DATA ROUTE
@app.route("/data")
def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "live_data.json")

    try:
        with open(file_path, "r") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"nifty": "-", "ce": "-", "pe": "-", "signal": "NO DATA"})

# Run server
def run_dashboard():
    app.run(host="0.0.0.0", port=5000)