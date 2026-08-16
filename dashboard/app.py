from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

# ----------------------------
# APP CONFIG
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "live_data.json")
CONFIG_FILE = os.path.join(BASE_DIR, "user_config.json")

app = Flask(__name__, template_folder="templates")


# ----------------------------
# HOME PAGE
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# LIVE MARKET DATA (BOT → UI)
# ----------------------------
@app.route("/data")
def get_data():
    try:
        with open(DATA_FILE, "r") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({
            "error": "No data yet",
            "message": str(e)
        })


# ----------------------------
# USER CONFIG (TOKEN / CLIENT ID)
# ----------------------------
@app.route("/config", methods=["GET", "POST"])
def config():
    # SAVE CONFIG
    if request.method == "POST":
        data = request.json

        config_data = {
            "client_id": data.get("client_id"),
            "access_token": data.get("access_token"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

        return jsonify({"status": "saved"})

    # GET CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({})


# ----------------------------
# HEALTH CHECK (for Render)
# ----------------------------
@app.route("/health")
def health():
    return jsonify({"status": "running"})


# ----------------------------
# RUN SERVER (LOCAL + CLOUD)
# ----------------------------
def run_dashboard():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ----------------------------
# ENTRY POINT (RENDER NEEDS THIS)
# ----------------------------
if __name__ == "__main__":
    run_dashboard()