import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given dataset.
    
    Args:
        data (pd.Series): Series of close prices.
        window (int): Look-back period for RSI calculation.
    
    Returns:
        pd.Series: RSI values.
    """
    # Calculate daily price changes
    delta = data.diff()

    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate average gain and loss
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    # Compute the Relative Strength (RS)
    rs = avg_gain / avg_loss

    # Compute RSI
    rsi = 100 - (100 / (1 + rs))

    return rsi

def plot_rsi(stock_symbol, start_date, end_date, window=14):
    """
    Plot RSI along with closing price for a stock/crypto.
    
    Args:
        stock_symbol (str): Ticker symbol (e.g., 'BTC-USD').
        start_date (str): Start date for historical data (e.g., '2020-01-01').
        end_date (str): End date for historical data (e.g., '2023-01-01').
        window (int): Look-back period for RSI calculation.
    """
    # Download historical data
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    if 'Close' not in data:
        print("Close price data is missing.")
        return

    # Calculate RSI
    data['RSI'] = calculate_rsi(data['Close'], window)

    # Plot closing price and RSI
    plt.figure(figsize=(14, 10))

    # Plot closing price
    plt.subplot(2, 1, 1)
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.title(f"{stock_symbol} - Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()

    # Plot RSI
    plt.subplot(2, 1, 2)
    plt.plot(data.index, data['RSI'], label='RSI', color='orange')
    plt.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    plt.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    plt.title(f"{stock_symbol} - Relative Strength Index (RSI)")
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    stock_symbol = "BTC-USD"  # Replace with your desired symbol
    start_date = "2020-01-01"
    end_date = "2024-12-30"
    plot_rsi(stock_symbol, start_date, end_date)
