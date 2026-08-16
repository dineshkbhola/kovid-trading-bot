def detect_market(data):
    price = data[-1]["close"]
    avg = sum([d["close"] for d in data]) / len(data)

    if price > avg * 1.002:
        return "TREND_UP"
    elif price < avg * 0.998:
        return "TREND_DOWN"
    else:
        return "SIDEWAYS"
