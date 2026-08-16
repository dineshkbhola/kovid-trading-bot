import requests
import pandas as pd

print("🚀 DOWNLOADING DHAN INSTRUMENT MASTER...")

url = "https://images.dhan.co/api-data/api-scrip-master.csv"

file_name = "instrument_master.csv"

try:
    r = requests.get(url)

    with open(file_name, "wb") as f:
        f.write(r.content)

    print("✅ Downloaded:", file_name)

    df = pd.read_csv(file_name)

    print("📊 Total Instruments:", len(df))

    # Filter NIFTY OPTIONS
    nifty_opt = df[
        (df['SEM_TRADING_SYMBOL'].str.contains("NIFTY")) &
        (df['SEM_INSTRUMENT_NAME'] == "OPTIDX")
    ]

    nifty_opt.to_csv("nifty_option_master.csv", index=False)

    print("✅ Saved Nifty Options:", len(nifty_opt))

except Exception as e:
    print("❌ ERROR:", e)