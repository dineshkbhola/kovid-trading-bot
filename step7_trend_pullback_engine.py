import pandas as pd

TARGET = 40
SL = 20


def load_data(path):
    df = pd.read_csv(path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    return df


def indicators(df):
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()

    df['rsi'] = calculate_rsi(df['close'], 14)
    return df


def calculate_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))


def run_backtest(df):

    trades = []
    position = None

    for i in range(50, len(df)):

        row = df.iloc[i]

        # -------------------------
        # TREND
        # -------------------------
        bullish = row['ema20'] > row['ema50']
        bearish = row['ema20'] < row['ema50']

        # -------------------------
        # PULLBACK ENTRY
        # -------------------------
        if position is None:

            # BUY pullback
            if bullish and row['rsi'] < 40:

                entry = row['close']
                position = {
                    'type': 'BUY',
                    'entry': entry,
                    'sl': entry - SL,
                    'target': entry + TARGET
                }

            # SELL pullback
            elif bearish and row['rsi'] > 60:

                entry = row['close']
                position = {
                    'type': 'SELL',
                    'entry': entry,
                    'sl': entry + SL,
                    'target': entry - TARGET
                }

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

    print("\n===== PHASE 7 TREND SYSTEM =====")
    print(f"Total Trades: {len(trades)}")
    print(f"Wins: {len(wins)} | Losses: {len(losses)}")

    if len(trades) > 0:
        print(f"Win Rate: {len(wins)/len(trades)*100:.2f}%")

    print(f"Total PnL: {sum(trades)}")


if __name__ == "__main__":

    file = "C:/Users/dines/OneDrive/Desktop/KovidTradingBot/nifty_5min_data.csv"

    df = load_data(file)
    df = indicators(df)

    trades = run_backtest(df)
    report(trades)