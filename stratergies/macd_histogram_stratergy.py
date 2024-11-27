import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fetch historical Bitcoin data
def fetch_bitcoin_data():
    # Get the last 1 year of data for Bitcoin
    data = yf.download('BTC-USD', period="1y", interval="1d")
    return data

# Calculate MACD, Signal Line, and Histogram
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    # Calculate the MACD line
    data['EMA_fast'] = data['Close'].ewm(span=fast_period, adjust=False).mean()
    data['EMA_slow'] = data['Close'].ewm(span=slow_period, adjust=False).mean()
    data['MACD'] = data['EMA_fast'] - data['EMA_slow']
    
    # Calculate the Signal line
    data['Signal_Line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()
    
    # Calculate the MACD Histogram (difference between MACD and Signal Line)
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    
    return data

# Generate buy/sell signals based on MACD Histogram
def generate_signals(data):
    # Buy signal when the MACD histogram is positive and crosses above the zero line
    data['Buy_Signal'] = np.where((data['MACD_Histogram'] > 0) & (data['MACD_Histogram'].shift(1) <= 0), 1, 0)
    
    # Sell signal when the MACD histogram is negative and crosses below the zero line
    data['Sell_Signal'] = np.where((data['MACD_Histogram'] < 0) & (data['MACD_Histogram'].shift(1) >= 0), 1, 0)
    
    return data

# Plot the results
def plot_macd_histogram(data):
    plt.figure(figsize=(12, 6))
    
    # Plot price and buy/sell signals
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(data['Close'], label='BTC-USD', color='blue')
    ax1.set_title("Bitcoin Price and Buy/Sell Signals")
    
    # Plot MACD Histogram
    ax2 = plt.subplot(2, 1, 2)
    ax2.bar(data.index, data['MACD_Histogram'], color='gray', label='MACD Histogram', width=0.6)
    
    # Highlight Buy and Sell Signals
    buy_signals = data[data['Buy_Signal'] == 1]
    sell_signals = data[data['Sell_Signal'] == 1]
    
    ax2.plot(buy_signals.index, buy_signals['MACD_Histogram'], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    ax2.plot(sell_signals.index, sell_signals['MACD_Histogram'], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    
    plt.legend(loc="best")
    plt.show()

if __name__ == "__main__":
    # Step 1: Fetch Bitcoin data
    data = fetch_bitcoin_data()
    
    # Step 2: Calculate MACD, Signal Line, and Histogram
    data = calculate_macd(data)
    
    # Step 3: Generate Buy/Sell signals based on MACD Histogram
    data = generate_signals(data)
    
    # Step 4: Plot the results
    plot_macd_histogram(data)
