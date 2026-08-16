import requests
import json
import os
import time

# ==============================
# CONFIG LOADER
# ==============================

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_headers():
    config = load_config()
    return {
        "access-token": config["ACCESS_TOKEN"],
        "client-id": config["CLIENT_ID"],
        "Content-Type": "application/json"
    }

# ==============================
# MANUAL ATM (TEMP FIX)
# ==============================

def get_manual_atm():
    # You can adjust this once daily if needed
    return 25000  # FIXED ATM FOR TESTING

# ==============================
# OPTION DATA COLLECTION
# ==============================

def collect_multi_option_data():

    print("🚀 STEP 9: STABLE OPTION DATA COLLECTION")

    atm = get_manual_atm()

    strikes = [atm - 100, atm - 50, atm, atm + 50, atm + 100]

    print("USING ATM:", atm)
    print("TRACKING STRIKES:", strikes)

    collected_data = []

    for strike in strikes:

        for option_type in ["CE", "PE"]:

            try:
                url = "https://api.dhan.co/v2/charts/historical"

                payload = {
                    "securityId": "13",  # TEMP (index test)
                    "exchangeSegment": "IDX_I",
                    "instrument": option_type,
                    "interval": "5m",
                    "fromDate": "2025-01-01",
                    "toDate": "2025-01-05"
                }

                r = requests.post(url, headers=get_headers(), json=payload)

                if r.status_code == 200:
                    data = r.json()

                    print(f"✅ {strike} {option_type} fetched")

                    collected_data.append({
                        "strike": strike,
                        "type": option_type,
                        "data": data
                    })
                else:
                    print(f"❌ Failed {strike} {option_type}", r.text)

            except Exception as e:
                print(f"ERROR {strike} {option_type}:", e)

            time.sleep(0.5)

    # Save file
    with open("option_data.json", "w") as f:
        json.dump(collected_data, f)

    print("✅ DATA SAVED: option_data.json")

# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    collect_multi_option_data()