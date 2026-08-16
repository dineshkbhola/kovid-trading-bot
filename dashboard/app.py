from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    with open("dashboard/live_data.json") as f:
        data = json.load(f)
    return render_template("index.html", data=data)

@app.route("/data")
def data():
    with open("dashboard/live_data.json") as f:
        return jsonify(json.load(f))