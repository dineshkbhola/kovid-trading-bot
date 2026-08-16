import json
import os
import time
import random

# Path to dashboard file
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "dashboard",
    "live_data.json"
)

def update_ui(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def simulate_data():
    print("🚀 UI Bridge Running...")

    while True:
        data = {
            "nifty": random.randint(24950, 25100),
            "atm": 25000,
            "ce": random.randint(80, 150),
            "pe": random.randint(80, 150),
            "signal": random.choice(["BUY CE", "BUY PE", "WAIT"])
        }

        update_ui(data)
        print("Updated UI:", data)

        time.sleep(2)

if __name__ == "__main__":
    simulate_data()