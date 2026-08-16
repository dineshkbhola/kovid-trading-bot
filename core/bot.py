import time
from core.data import get_price
from core.regime import detect_market
from core.strategy import generate_signal
from core.paper import execute_trade

def run_bot():
    data = []
    while True:
        price = get_price()
        if price is None:
            continue

        data.append({"close": price})

        if len(data) < 10:
            time.sleep(1)
            continue

        market = detect_market(data)
        signal = generate_signal(data, market)

        trade = execute_trade(signal, price)

        if trade:
            print("Trade:", trade, "| Market:", market)

        time.sleep(2)
