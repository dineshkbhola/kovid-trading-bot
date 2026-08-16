import pandas as pd

TARGET = 50
SL = 20


def load_data(path):
    df = pd.read_csv(path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    return df


def prepare_levels(df):
    df['prev_high'] = df['high'].shift(1).rolling(75).max()
    df['prev_low'] = df['low'].shift(1).rolling(75).min()
    return df


def run_backtest(df):

    trades = []
    position = None

    breakout_level = None
    breakout_type = None

    for i in range(100, len(df)):

        row = df.iloc[i]
        prev = df.iloc[i-1]

        # -------------------------
        # DETECT BREAKOUT
        # -------------------------
        if breakout_type is None:

            # Bullish breakout
            if row['close'] > row['prev_high']:
                breakout_type = "BUY"
                breakout_level = row['prev_high']
                continue

            # Bearish breakout
            elif row['close'] < row['prev_low']:
                breakout_type = "SELL"
                breakout_level = row['prev_low']
                continue

        # -------------------------
        # RETEST ENTRY (EDGE)
        # -------------------------
        if breakout_type == "BUY" and position is None:

            # price comes back and holds
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
        # EXIT LOGIC
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

    print("\n===== PHASE 4 BACKTEST =====")
    print(f"Total Trades: {len(trades)}")
    print(f"Wins: {len(wins)} | Losses: {len(losses)}")

    if len(trades) > 0:
        print(f"Win Rate: {len(wins)/len(trades)*100:.2f}%")

    print(f"Total PnL: {sum(trades)}")


if __name__ == "__main__":

    file = "C:/Users/dines/OneDrive/Desktop/KovidTradingBot/nifty_5min_data.csv"

    df = load_data(file)
    df = prepare_levels(df)

    trades = run_backtest(df)
    report(trades)