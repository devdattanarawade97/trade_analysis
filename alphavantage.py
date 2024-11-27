import os
import requests
import csv
import json

def get_crypto_historical_data(api_key, symbol, market):
    """
    Fetch historical cryptocurrency data from Alpha Vantage.
    
    Args:
        api_key (str): Your Alpha Vantage API key.
        symbol (str): The cryptocurrency symbol (e.g., 'BTC').
        market (str): The market to convert to (e.g., 'USD').
    
    Returns:
        dict: Historical cryptocurrency data.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": symbol,
        "market": market,
        "apikey": api_key
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Digital Currency Daily)" in data:
            return data["Time Series (Digital Currency Daily)"]
        else:
            print("Error:", data.get("Note", "No data available."))
            return None
    else:
        print(f"HTTP Error {response.status_code}: {response.reason}")
        return None

def save_to_csv(data, file_name):
    """
    Save historical cryptocurrency data to a CSV file.
    
    Args:
        data (dict): The historical cryptocurrency data.
        file_name (str): The name of the output CSV file.
    """
    if not data:
        print("No data to save.")
        return
    
    # Define the header row based on the data structure (the keys of the first date entry)
    headers = ["Date", "1. open", "2. high", "3. low", "4. close", "5. volume"]
    
    # Open the file in write mode
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(headers)
        
        # Write each data row
        for date, values in sorted(data.items(), reverse=True):  # Sort by date descending
            row = [date] + [values.get(header, "") for header in headers[1:]]
            writer.writerow(row)
    
    print(f"Data saved to {file_name}")

if __name__ == "__main__":
    # Replace with your Alpha Vantage API key
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY")  # or replace with your key directly
    symbol = "BTC"  # Cryptocurrency symbol
    market = "USD"  # Market symbol
    
    # Fetch the historical data
    historical_data = get_crypto_historical_data(api_key, symbol, market)
    
    if historical_data:
        # Save the data to a CSV file
        save_to_csv(historical_data, "crypto_historical_data.csv")
