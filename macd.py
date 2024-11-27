import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch Bitcoin data from Yahoo Finance
symbol = "BTC-USD"  # Bitcoin symbol on Yahoo Finance
data = yf.download(symbol, start="2020-01-01", end="2026-12-31")

# Calculate MACD and Signal Line
data['12_EMA'] = data['Close'].ewm(span=12, adjust=False).mean()  # 12-day EMA
data['26_EMA'] = data['Close'].ewm(span=26, adjust=False).mean()  # 26-day EMA
data['MACD'] = data['12_EMA'] - data['26_EMA']  # MACD Line
data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()  # Signal Line (9-day EMA)

# Plot the MACD and Signal Line
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['MACD'], label='MACD Line', color='blue')
plt.plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
plt.title(f'MACD for Bitcoin ({symbol})')
plt.legend(loc='upper left')
plt.show()
