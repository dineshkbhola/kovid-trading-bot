import pandas as pd

print("🚀 STEP 11: OPTION RESOLVER ENGINE")

# Load option master
df = pd.read_csv("nifty_option_master.csv", low_memory=False)

# Clean columns
df = df[['SEM_TRADING_SYMBOL', 'SEM_STRIKE_PRICE', 'SEM_EXPIRY_DATE', 'SEM_OPTION_TYPE', 'SEM_SMST_SECURITY_ID']]

# Convert types
df['SEM_STRIKE_PRICE'] = pd.to_numeric(df['SEM_STRIKE_PRICE'], errors='coerce')
df['SEM_EXPIRY_DATE'] = pd.to_datetime(df['SEM_EXPIRY_DATE'], errors='coerce')

# Drop bad rows
df = df.dropna()

# Sort expiry
df = df.sort_values('SEM_EXPIRY_DATE')

def get_atm_strike(price):
    return round(price / 50) * 50

def get_nearest_expiry():
    return df['SEM_EXPIRY_DATE'].iloc[0]

def resolve_option(price):
    atm = get_atm_strike(price)
    expiry = get_nearest_expiry()

    print(f"📊 NIFTY PRICE: {price}")
    print(f"🎯 ATM STRIKE: {atm}")
    print(f"📅 EXPIRY: {expiry.date()}")

    ce = df[
        (df['SEM_STRIKE_PRICE'] == atm) &
        (df['SEM_OPTION_TYPE'] == 'CE') &
        (df['SEM_EXPIRY_DATE'] == expiry)
    ]

    pe = df[
        (df['SEM_STRIKE_PRICE'] == atm) &
        (df['SEM_OPTION_TYPE'] == 'PE') &
        (df['SEM_EXPIRY_DATE'] == expiry)
    ]

    if ce.empty or pe.empty:
        print("❌ ERROR: Option not found")
        return None

    ce_id = ce.iloc[0]['SEM_SMST_SECURITY_ID']
    pe_id = pe.iloc[0]['SEM_SMST_SECURITY_ID']

    print("✅ CE ID:", ce_id)
    print("✅ PE ID:", pe_id)

    return ce_id, pe_id


# TEST RUN
if __name__ == "__main__":
    # Example price (you can change)
    resolve_option(25000)