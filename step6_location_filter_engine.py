import pandas as pd

TARGET = 50
SL = 20


def load_data(path):
    df = pd.read_csv(path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    return df


def prepare(df):

    df['date'] = df.index.date

    # Previous day high/low
    df['prev_day_high'] = df.groupby('date')['high'].transform('max').shift(75)
    df['prev_day_low'] = df.groupby('date')['low'].transform('min').shift(75)

    # candle strength
    df['range'] = df['high'] - df['low']
    df['body'] = abs(df['close'] - df['open'])

    return df


def strong_candle(row):
    return row['body'] > row['range'] * 0.6


def near_level(price, level, buffer=20):
    return abs(price - level) <= buffer


def run_backtest(df):

    trades = []
    position = None

    breakout_type = None
    breakout_level = None

    for i in range(100, len(df)):

        row = df.iloc[i]

        # -------------------------
        # LOCATION FILTER
        # -------------------------
        near_high = near_level(row['close'], row['prev_day_high'])
        near_low = near_level(row['close'], row['prev_day_low'])

        # -------------------------
        # BREAKOUT DETECTION
        # -------------------------
        if breakout_type is None:

            # BUY only near resistance break
            if near_high and row['close'] > row['prev_day_high']:

                if strong_candle(row):
                    breakout_type = "BUY"
                    breakout_level = row['prev_day_high']
                continue

            # SELL only near support break
            elif near_low and row['close'] < row['prev_day_low']:

                if strong_candle(row):
                    breakout_type = "SELL"
                    breakout_level = row['prev_day_low']
                continue

        # -------------------------
        # RETEST ENTRY
        # -------------------------
        if breakout_type == "BUY" and position is None:

            if row['low'] <= breakout_level and row['close'] > breakout_level:

                entry = row['close']
                position = {
                    'type': 'BUY',
                    'entry': entry,
                    'sl': entry - SL,
                    'target': entry + TARGET
                }

                breakout_type = None

        elif breakout_type == "SELL" and position is None:

            if row['high'] >= breakout_level and row['close'] < breakout_level:

                entry = row['close']
                position = {
                    'type': 'SELL',
                    'entry': entry,
                    'sl': entry + SL,
                    'target': entry - TARGET
                }

                breakout_type = None

        # -------------------------
        # EXIT
        # -------------------------
        if position:

            if position['type'] == 'BUY':

                if row['low'] <= position['sl']:
                    trades.append(-SL)
                    position = None

                elif row['high'] >= position['target']:
                    trades.append(TARGET)
                    position = None

            elif position['type'] == 'SELL':

                if row['high'] >= position['sl']:
                    trades.append(-SL)
                    position = None

                elif row['low'] <= position['target']:
                    trades.append(TARGET)
                    position = None

    return trades


def report(trades):

    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]

    print("\n===== PHASE 6 BACKTEST =====")
    print(f"Total Trades: {len(trades)}")
    print(f"Wins: {len(wins)} | Losses: {len(losses)}")

    if len(trades) > 0:
        print(f"Win Rate: {len(wins)/len(trades)*100:.2f}%")

    print(f"Total PnL: {sum(trades)}")


if __name__ == "__main__":

    file = "C:/Users/dines/OneDrive/Desktop/KovidTradingBot/nifty_5min_data.csv"

    df = load_data(file)
    df = prepare(df)

    trades = run_backtest(df)
    report(trades)