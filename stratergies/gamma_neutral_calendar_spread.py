import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_options_data(symbol="BTCUSDT"):
    """Fetch BTC options data from Binance Vanilla Options API."""
    base_url = "https://vapi.binance.com"
    endpoint = "/vapi/v1/optionInfo"

    params = {
        "underlying": symbol,  # Symbol for the underlying asset
    }

    response = requests.get(base_url + endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        if "data" in data and "optionContracts" in data["data"]:
            options_list = []
            for contract in data["data"]["optionContracts"]:
                options_list.append({
                    "symbol": contract["symbol"],
                    "expiry": contract["expiryDate"],
                    "strike": float(contract["strike"]),
                    "markPrice": float(contract["markPrice"]) if "markPrice" in contract else 0.0
                })
            return pd.DataFrame(options_list)
        else:
            print("No option contracts found in the API response.")
            return pd.DataFrame()
    else:
        print("Failed to fetch options data:", response.text)
        return pd.DataFrame()

def gamma_neutral_calendar_spread(options_data, short_days=7, long_days=30):
    today = datetime.utcnow()
    short_expiry = today + timedelta(days=short_days)
    long_expiry = today + timedelta(days=long_days)
    
    options_data['expiry'] = pd.to_datetime(options_data['expiry'], unit='ms')
    
    short_options = options_data[options_data['expiry'] == short_expiry]
    long_options = options_data[options_data['expiry'] == long_expiry]
    
    results = []
    for _, short_row in short_options.iterrows():
        strike = short_row['strike']
        short_price = short_row['markPrice']
        long_row = long_options[long_options['strike'] == strike]
        if long_row.empty:
            continue
        
        long_price = long_row.iloc[0]['markPrice']
        net_cost = long_price - short_price
        max_profit = short_price - net_cost
        max_loss = net_cost
        monthly_profit = max_profit - max_loss
        
        results.append({
            "strike": strike,
            "short_price": short_price,
            "long_price": long_price,
            "net_cost": net_cost,
            "max_profit": max_profit,
            "max_loss": max_loss,
            "monthly_profit": monthly_profit,
        })
    return pd.DataFrame(results)

def calculate_apy(df, capital):
    df['apy'] = (df['monthly_profit'] / capital) * 12 * 100
    return df

# Fetch options data
options_data = fetch_options_data()
if options_data.empty:
    print("No options data available. Exiting.")
    exit()

spread_results = gamma_neutral_calendar_spread(options_data)
spread_results = calculate_apy(spread_results, 1000)
spread_results.to_csv("gamma_neutral_results.csv", index=False)
print("Results saved to gamma_neutral_results.csv")
