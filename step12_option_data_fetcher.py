import requests
import pandas as pd
import json
from datetime import datetime, timedelta

print("🚀 STEP 12: REAL OPTION DATA FETCHER")

# ==============================
# CONFIG LOADER (AUTO TOKEN)
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
# FETCH HISTORICAL DATA
# ==============================
def fetch_option_data(security_id):
    url = "https://api.dhan.co/v2/charts/intraday"

    to_date = datetime.now()
    from_date = to_date - timedelta(days=2)

    payload = {
        "securityId": str(security_id),
        "exchangeSegment": "NSE_FNO",
        "instrument": "OPTIDX",
        "interval": "5",
        "fromDate": from_date.strftime("%Y-%m-%d"),
        "toDate": to_date.strftime("%Y-%m-%d")
    }

    try:
        r = requests.post(url, headers=get_headers(), json=payload)

        if r.status_code != 200:
            print(f"❌ API ERROR {r.status_code}: {r.text}")
            return None

        data = r.json()

        if "close" not in data:
            print("❌ No data received")
            return None

        df = pd.DataFrame({
            "time": data["timestamp"],
            "open": data["open"],
            "high": data["high"],
            "low": data["low"],
            "close": data["close"],
            "volume": data["volume"]
        })

        print(f"✅ Data fetched for {security_id} | Rows: {len(df)}")

        return df

    except Exception as e:
        print("❌ ERROR:", e)
        return None

# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":

    # USE YOUR STEP 11 OUTPUT IDS
    CE_ID = 45148
    PE_ID = 45149

    ce_df = fetch_option_data(CE_ID)
    pe_df = fetch_option_data(PE_ID)

    if ce_df is not None:
        ce_df.to_csv("ce_data.csv", index=False)
        print("📁 Saved CE data")

    if pe_df is not None:
        pe_df.to_csv("pe_data.csv", index=False)
        print("📁 Saved PE data")