def generate_signal(data, market):
    if market == "TREND_UP":
        return {"action": "BUY", "type": "CE"}
    elif market == "TREND_DOWN":
        return {"action": "BUY", "type": "PE"}
    return {"action": None}
