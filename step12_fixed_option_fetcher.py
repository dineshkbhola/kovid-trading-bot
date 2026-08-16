import requests
import pandas as pd
import json
from datetime import datetime

print("🚀 STEP 12 FIXED: LIVE SESSION OPTION FETCHER")

# ==============================
# CONFIG
# ==============================
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def get_headers():
    config = load_config()
    return {
        "access-token": config["ACCESS_TOKEN"],
        "client-id": config["CLIENT_ID"],
        "Content-Type": "application/json"
    }

# ==============================
# FETCH DATA (TODAY ONLY)
# ==============================
def fetch_option_data(security_id):
    url = "https://api.dhan.co/v2/charts/intraday"

    today = datetime.now().strftime("%Y-%m-%d")

    payload = {
        "securityId": str(security_id),
        "exchangeSegment": "NSE_FNO",
        "instrument": "OPTIDX",
        "interval": "5",
        "fromDate": today,
        "toDate": today
    }

    r = requests.post(url, headers=get_headers(), json=payload)

    if r.status_code != 200:
        print(f"❌ API ERROR {r.status_code}: {r.text}")
        return None

    data = r.json()

    if "close" not in data or len(data["close"]) == 0:
        print("❌ No intraday data available (market closed or wrong contract)")
        return None

    df = pd.DataFrame({
        "time": data["timestamp"],
        "open": data["open"],
        "high": data["high"],
        "low": data["low"],
        "close": data["close"],
        "volume": data["volume"]
    })

    print(f"✅ SUCCESS: {security_id} | Rows: {len(df)}")
    return df

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":

    CE_ID = 45148
    PE_ID = 45149

    ce = fetch_option_data(CE_ID)
    pe = fetch_option_data(PE_ID)

    if ce is not None:
        ce.to_csv("ce_today.csv", index=False)
        print("📁 CE saved")

    if pe is not None:
        pe.to_csv("pe_today.csv", index=False)
        print("📁 PE saved")