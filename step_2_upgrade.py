import os

CODE = """import pandas as pd
import numpy as np

TARGET = 50
SL = 20
MAX_TRADES_PER_DAY = 2

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def run_backtest(file_path):
    df = pd.read_csv(file_path)

    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Indicators
    df['EMA20'] = df['close'].ewm(span=20).mean()
    df['EMA50'] = df['close'].ewm(span=50).mean()
    df = calculate_rsi(df)

    trades = []
    trade_count = {}
    position = None
    breakout = None
    breakout_level = None

    for i in range(50, len(df)):
        row = df.iloc[i]

        day = row.name.date()
        if day not in trade_count:
            trade_count[day] = 0

        if trade_count[day] >= MAX_TRADES_PER_DAY:
            continue

        # TIME FILTER
        t = row.name.time()
        if not ((t >= pd.to_datetime("09:20").time() and t <= pd.to_datetime("11:00").time()) or
                (t >= pd.to_datetime("13:30").time() and t <= pd.to_datetime("14:45").time())):
            continue

        # LEVELS
        resistance = df.iloc[i-20:i]['high'].max()
        support = df.iloc[i-20:i]['low'].min()

        body = abs(row['close'] - row['open'])
        candle_range = row['high'] - row['low']

        # STRONG BREAKOUT
        if candle_range > 0:
            strength = body / candle_range
        else:
            strength = 0

        if row['close'] > resistance and strength > 0.6:
            breakout = "bullish"
            breakout_level = resistance

        elif row['close'] < support and strength > 0.6:
            breakout = "bearish"
            breakout_level = support

        # ENTRY FILTERS
        if breakout == "bullish" and position is None:
            if row['low'] <= breakout_level and row['close'] > breakout_level:
                if row['RSI'] > 60 and row['EMA20'] > row['EMA50']:

                    entry = row['close']
                    position = {
                        "type": "BUY",
                        "entry": entry,
                        "sl": entry - SL,
                        "target": entry + TARGET
                    }
                    trade_count[day] += 1

        elif breakout == "bearish" and position is None:
            if row['high'] >= breakout_level and row['close'] < breakout_level:
                if row['RSI'] < 40 and row['EMA20'] < row['EMA50']:

                    entry = row['close']
                    position = {
                        "type": "SELL",
                        "entry": entry,
                        "sl": entry + SL,
                        "target": entry - TARGET
                    }
                    trade_count[day] += 1

        # EXIT
        if position:
            if position["type"] == "BUY":
                if row['low'] <= position["sl"]:
                    trades.append(-SL)
                    position = None
                elif row['high'] >= position["target"]:
                    trades.append(TARGET)
                    position = None

            elif position["type"] == "SELL":
                if row['high'] >= position["sl"]:
                    trades.append(-SL)
                    position = None
                elif row['low'] <= position["target"]:
                    trades.append(TARGET)
                    position = None

    total = sum(trades)
    wins = len([t for t in trades if t > 0])
    losses = len([t for t in trades if t < 0])

    print("\\n===== PHASE 2 BACKTEST =====")
    print(f"Total Trades: {len(trades)}")
    print(f"Wins: {wins} | Losses: {losses}")
    print(f"Win Rate: {(wins / len(trades) * 100) if trades else 0:.2f}%")
    print(f"Total PnL: {total}")
"""

# WRITE FILE
path = "core/backtest.py"

with open(path, "w") as f:
    f.write(CODE)

print("✅ Phase 2 Installed Successfully!")
print("➡ File Updated: core/backtest.py")