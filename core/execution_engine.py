import time
import json
import os
import random

# ---------------------------
# LOAD CONFIG (TOKEN SYSTEM)
# ---------------------------
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

# ---------------------------
# UPDATE DASHBOARD JSON
# ---------------------------
def update_dashboard(data):
    path = os.path.join("dashboard", "live_data.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# GENERATE TRADE SIGNAL (TEMP)
# ---------------------------
def get_signal():
    return random.choice(["BUY CE", "BUY PE", "WAIT"])

# ---------------------------
# PLACE ORDER (SIMULATION)
# ---------------------------
def place_order(signal):
    if signal == "WAIT":
        return None

    order_id = f"ORD{random.randint(10000,99999)}"

    entry_price = random.randint(180, 220)

    trade = {
        "order_id": order_id,
        "signal": signal,
        "entry": entry_price,
        "target": entry_price + 20,
        "stoploss": entry_price - 20,
        "lots": 3,
        "status": "PLACED"
    }

    print(f"🚀 ORDER PLACED: {trade}")
    return trade

# ---------------------------
# TRACK ORDER (SIMULATION)
# ---------------------------
def track_order(trade):
    print("⏳ Tracking order...")

    time.sleep(2)

    trade["status"] = "EXECUTED"
    print(f"✅ EXECUTED at {trade['entry']}")

    return trade

# ---------------------------
# MONITOR TRADE (TARGET/SL)
# ---------------------------
def monitor_trade(trade):
    print("📊 Monitoring trade...")

    current_price = trade["entry"]

    while True:
        time.sleep(2)

        move = random.randint(-10, 10)
        current_price += move

        pnl = (current_price - trade["entry"]) * trade["lots"] * 50

        print(f"Price: {current_price} | PnL: {pnl}")

        # Update dashboard
        update_dashboard({
            "nifty": random.randint(24900, 25100),
            "signal": trade["signal"],
            "entry": trade["entry"],
            "current": current_price,
            "target": trade["target"],
            "stoploss": trade["stoploss"],
            "pnl": pnl,
            "status": trade["status"]
        })

        # TARGET HIT
        if current_price >= trade["target"]:
            print("🎯 TARGET HIT")
            trade["status"] = "TARGET HIT"
            break

        # STOPLOSS HIT
        if current_price <= trade["stoploss"]:
            print("🛑 STOPLOSS HIT")
            trade["status"] = "STOPLOSS HIT"
            break

    return trade

# ---------------------------
# MAIN ENGINE LOOP
# ---------------------------
def run_execution_engine():
    print("🚀 STEP 15: EXECUTION ENGINE STARTED")

    while True:
        signal = get_signal()

        print(f"📡 Signal: {signal}")

        trade = place_order(signal)

        if trade:
            trade = track_order(trade)
            trade = monitor_trade(trade)

            print(f"📦 FINAL STATUS: {trade['status']}")

        time.sleep(5)


# ---------------------------
# RUN
# ---------------------------
if __name__ == "__main__":
    run_execution_engine()