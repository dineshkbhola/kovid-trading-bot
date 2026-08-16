trades = []
def execute_trade(signal, price):
    if signal["action"] is None:
        return None

    trade = {
        "entry": price,
        "exit": price + 10 if signal["type"] == "CE" else price - 10,
        "type": signal["type"]
    }
    trades.append(trade)
    return trade
