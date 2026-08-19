from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Path to live data file
DATA_FILE = os.path.join(os.path.dirname(__file__), "live_data.json")


# -----------------------------
# HOME ROUTE (DASHBOARD UI)
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# LIVE DATA API (FOR UI REFRESH)
# -----------------------------
@app.route("/data")
def data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({
            "nifty": 0,
            "ce_price": 0,
            "pe_price": 0,
            "signal": "WAIT",
            "status": "NO DATA"
        })


# -----------------------------
# HEALTH CHECK (OPTIONAL)
# -----------------------------
@app.route("/health")
def health():
    return "OK"


# -----------------------------
# RUN SERVER (RENDER COMPATIBLE)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
