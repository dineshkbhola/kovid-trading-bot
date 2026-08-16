import pandas as pd
import json

print("🚀 STEP 10 PRO: BUILDING OPTION MASTER")

# ==============================
# LOAD CSV
# ==============================

file_path = "../instrument_master.csv"

df = pd.read_csv(file_path)

print("TOTAL ROWS:", len(df))

# ==============================
# FILTER NIFTY OPTIONS
# ==============================

nifty_options = df[
    (df["SEM_EXM_EXCH_ID"] == "NSE") &
    (df["SEM_SEGMENT"] == "NSE FNO") &
    (df["SEM_INSTRUMENT_NAME"] == "OPTIDX") &
    (df["SEM_TRADING_SYMBOL"].str.contains("NIFTY"))
]

print("NIFTY OPTIONS FOUND:", len(nifty_options))

# ==============================
# CLEAN DATA
# ==============================

result = []

for _, row in nifty_options.iterrows():
    result.append({
        "symbol": row["SEM_TRADING_SYMBOL"],
        "securityId": row["SEM_SMST_SECURITY_ID"],
        "strike": row["SEM_STRIKE_PRICE"],
        "expiry": row["SEM_EXPIRY_DATE"],
        "type": "CE" if "CE" in row["SEM_TRADING_SYMBOL"] else "PE"
    })

# ==============================
# SAVE JSON
# ==============================

with open("option_master.json", "w") as f:
    json.dump(result, f)

print("✅ option_master.json CREATED")