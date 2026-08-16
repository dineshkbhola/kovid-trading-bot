import pandas as pd

# SETTINGS
TARGET = 50
SL = 20
MAX_TRADES_PER_DAY = 3


def load_data(path):
    df = pd.read_csv(path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    return df


def add_indicators(df):
    df['ema20'] = df['close'].ewm(span=20).mean()
    df['ema50'] = df['close'].ewm(span=50).mean()

    df['rsi'] = calculate_rsi(df['close'], 14)
    df['vol_avg'] = df['volume'].rolling(20).mean()

    return df


def calculate_rsi(series, period):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()

    rs = gain / loss
    return 100 - (100 / (1 + rs))


def is_trending(df, i):
    return df['ema20'].iloc[i] > df['ema50'].iloc[i]


def run_backtest(df):

    trades = []
    position = None
    daily_trades = 0
    current_day = None

    for i in range(50, len(df)):

        row = df.iloc[i]
        prev = df.iloc[i-1]

        # Reset daily trade count
        day = row.name.date()
        if current_day != day:
            current_day = day
            daily_trades = 0

        if daily_trades >= MAX_TRADES_PER_DAY:
            continue

        # -------------------------
        # STRONG CANDLE FILTER
        # -------------------------
        body = abs(row['close'] - row['open'])
        range_candle = row['high'] - row['low']

        if body < (range_candle * 0.5):
            continue

        # -------------------------
        # TREND FILTER
        # -------------------------
        bullish_trend = row['ema20'] > row['ema50']
        bearish_trend = row['ema20'] < row['ema50']

        # -------------------------
        # VOLUME FILTER
        # -------------------------
        if row['volume'] < row['vol_avg']:
            continue

        # -------------------------
        # ENTRY CONDITIONS
        # -------------------------
        if position is None:

            # BUY
            if bullish_trend and row['rsi'] > 60:
                entry = row['close']
                position = {
                    'type': 'BUY',
                    'entry': entry,
                    'sl': entry - SL,
                    'target': entry + TARGET
                }
                daily_trades += 1

            # SELL
            elif bearish_trend and row['rsi'] < 40:
                entry = row['close']
                position = {
                    'type': 'SELL',
                    'entry': entry,
                    'sl': entry + SL,
                    'target': entry - TARGET
                }
                daily_trades += 1

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

    print("\n===== PHASE 3 BACKTEST =====")
    print(f"Total Trades: {len(trades)}")
    print(f"Wins: {len(wins)} | Losses: {len(losses)}")

    if len(trades) > 0:
        print(f"Win Rate: {len(wins)/len(trades)*100:.2f}%")

    print(f"Total PnL: {sum(trades)}")


if __name__ == "__main__":

    file = "C:/Users/dines/OneDrive/Desktop/KovidTradingBot/nifty_5min_data.csv"

    df = load_data(file)
    df = add_indicators(df)

    trades = run_backtest(df)
    report(trades)