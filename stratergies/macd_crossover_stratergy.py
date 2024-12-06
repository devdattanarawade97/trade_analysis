import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Fetch historical Bitcoin data
def fetch_bitcoin_data():
    # Get the last 1 year of data for Bitcoin
    data = yf.download('AMZN', period="1y", interval="1d")
    return data

# Calculate MACD and Signal Line
def calculate_macd(data, fast_period=12, slow_period=26, signal_period=9):
    # Calculate the MACD line
    data['EMA_fast'] = data['Close'].ewm(span=fast_period, adjust=False).mean()
    data['EMA_slow'] = data['Close'].ewm(span=slow_period, adjust=False).mean()
    data['MACD'] = data['EMA_fast'] - data['EMA_slow']
    
    # Calculate the Signal line
    data['Signal_Line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()
    
    return data

# Generate buy/sell signals based on MACD crossover
def generate_signals(data):
    # Buy signal when MACD crosses above Signal Line
    data['Buy_Signal'] = np.where(data['MACD'] > data['Signal_Line'], 1, 0)
    # Sell signal when MACD crosses below Signal Line
    data['Sell_Signal'] = np.where(data['MACD'] < data['Signal_Line'], 1, 0)
    
    # Identify the crossover points
    data['Buy_Crossover'] = (data['Buy_Signal'] == 1) & (data['Buy_Signal'].shift(1) == 0)
    data['Sell_Crossover'] = (data['Sell_Signal'] == 1) & (data['Sell_Signal'].shift(1) == 0)

    return data

# Plot the results
def plot_macd(data):
    plt.figure(figsize=(12, 6))
    
    # Plot price and buy/sell signals
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(data['Close'], label='BTC-USD', color='blue')
    ax1.set_title("Bitcoin Price and Buy/Sell Signals")
    
    # Plot MACD and Signal Line
    ax2 = plt.subplot(2, 1, 2)
    ax2.plot(data['MACD'], label='MACD', color='orange')
    ax2.plot(data['Signal_Line'], label='Signal Line', color='green')
    
    # Highlight Buy and Sell Crossovers
    ax2.plot(data[data['Buy_Crossover']].index, data['MACD'][data['Buy_Crossover']], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    ax2.plot(data[data['Sell_Crossover']].index, data['MACD'][data['Sell_Crossover']], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    
    plt.legend(loc="best")
    plt.show()

if __name__ == "__main__":
    # Step 1: Fetch Bitcoin data
    data = fetch_bitcoin_data()
    
    # Step 2: Calculate MACD and Signal Line
    data = calculate_macd(data)
    
    # Step 3: Generate Buy/Sell signals based on MACD crossover
    data = generate_signals(data)
    
    # Step 4: Plot the results
    plot_macd(data)
