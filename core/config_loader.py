import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config
    except Exception as e:
        print("CONFIG LOAD ERROR:", e)
        return {}

def get_auth_headers():
    config = load_config()

    return {
        "access-token": config.get("ACCESS_TOKEN"),
        "client-id": config.get("CLIENT_ID"),
        "Content-Type": "application/json"
    }