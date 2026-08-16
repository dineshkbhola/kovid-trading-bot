import requests
import pandas as pd
import json
import time
from datetime import datetime

print("🚀 STEP 13: LIVE OPTION DATA COLLECTOR STARTED")

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
# GET NIFTY PRICE
# ==============================
def get_nifty_price():
    url = "https://api.dhan.co/v2/charts/historical"

    payload = {
        "securityId": "13",
        "exchangeSegment": "IDX_I",
        "instrument": "INDEX",
        "interval": "1",
        "fromDate": datetime.now().strftime("%Y-%m-%d"),
        "toDate": datetime.now().strftime("%Y-%m-%d")
    }

    r = requests.post(url, headers=get_headers(), json=payload)

    data = r.json()

    return data["close"][-1]

# ==============================
# LOAD OPTION MASTER
# ==============================
df = pd.read_csv("nifty_option_master.csv", low_memory=False)
df['SEM_STRIKE_PRICE'] = pd.to_numeric(df['SEM_STRIKE_PRICE'], errors='coerce')
df['SEM_EXPIRY_DATE'] = pd.to_datetime(df['SEM_EXPIRY_DATE'], errors='coerce')
df = df.dropna()
df = df.sort_values('SEM_EXPIRY_DATE')

def get_option_ids(price):
    atm = round(price / 50) * 50
    expiry = df['SEM_EXPIRY_DATE'].iloc[0]

    ce = df[(df['SEM_STRIKE_PRICE'] == atm) & (df['SEM_OPTION_TYPE'] == 'CE') & (df['SEM_EXPIRY_DATE'] == expiry)]
    pe = df[(df['SEM_STRIKE_PRICE'] == atm) & (df['SEM_OPTION_TYPE'] == 'PE') & (df['SEM_EXPIRY_DATE'] == expiry)]

    return ce.iloc[0]['SEM_SMST_SECURITY_ID'], pe.iloc[0]['SEM_SMST_SECURITY_ID'], atm

# ==============================
# FETCH OPTION LTP
# ==============================
def get_option_ltp(security_id):
    url = "https://api.dhan.co/marketfeed/ltp"

    payload = {
        "NSE_FNO": [int(security_id)]
    }

    r = requests.post(url, headers=get_headers(), json=payload)

    try:
        data = r.json()
        return list(data.values())[0]["last_price"]
    except:
        return None

# ==============================
# MAIN LOOP
# ==============================
while True:
    try:
        now = datetime.now()

        # Only during market hours
        if now.hour < 9 or now.hour > 15:
            print("⏳ Waiting for market hours...")
            time.sleep(60)
            continue

        nifty = get_nifty_price()
        ce_id, pe_id, atm = get_option_ids(nifty)

        ce_price = get_option_ltp(ce_id)
        pe_price = get_option_ltp(pe_id)

        row = {
            "time": now,
            "nifty": nifty,
            "atm": atm,
            "ce_price": ce_price,
            "pe_price": pe_price
        }

        df_row = pd.DataFrame([row])

        file_name = "live_option_data.csv"

        try:
            df_existing = pd.read_csv(file_name)
            df_all = pd.concat([df_existing, df_row])
        except:
            df_all = df_row

        df_all.to_csv(file_name, index=False)

        print(f"✅ {now} | NIFTY: {nifty} | CE: {ce_price} | PE: {pe_price}")

        time.sleep(300)  # 5 min

    except Exception as e:
        print("❌ ERROR:", e)
        time.sleep(60)