import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def moving_average_crossover_strategy(stock_symbol, start_date, end_date, short_window=50, long_window=200):
    """
    Implements the Moving Average Crossover Strategy.

    Args:
        stock_symbol (str): Ticker symbol of the stock (e.g., 'BTC-USD').
        start_date (str): Start date for historical data (e.g., '2020-01-01').
        end_date (str): End date for historical data (e.g., '2023-01-01').
        short_window (int): Period for the short-term moving average.
        long_window (int): Period for the long-term moving average.
    """
    # Fetch historical stock data
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    
    # Calculate moving averages
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    
    # Generate buy/sell signals
    data['Signal'] = 0  # Default: No signal
    data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1  # Buy signal
    data.loc[data['Short_MA'] <= data['Long_MA'], 'Signal'] = -1  # Sell signal
    
    # Visualize the data
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['Short_MA'], label=f'{short_window}-Day MA', alpha=0.8)
    plt.plot(data['Long_MA'], label=f'{long_window}-Day MA', alpha=0.8)
    plt.scatter(data.index[data['Signal'] == 1], data['Close'][data['Signal'] == 1], label='Buy Signal', marker='^', color='green', alpha=1)
    plt.scatter(data.index[data['Signal'] == -1], data['Close'][data['Signal'] == -1], label='Sell Signal', marker='v', color='red', alpha=1)
    plt.title(f"Moving Average Crossover Strategy: {stock_symbol}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid()
    plt.show()
    
    return data

# Example usage
if __name__ == "__main__":
    stock_symbol = "BTC-USD"  # Replace with the stock/crypto symbol you want to analyze
    start_date = "2020-01-01"
    end_date = "2024-12-30"
    strategy_data = moving_average_crossover_strategy(stock_symbol, start_date, end_date)
