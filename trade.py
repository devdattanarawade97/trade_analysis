import yfinance as yf

# Define the stock ticker and time range
ticker = "AMZN"
start_date = "2024-09-01"  # Replace with desired start date
end_date = "2024-10-26"    # Replace with desired end date

# Fetch historical data
data = yf.download(ticker, start=start_date, end=end_date)

# Display the first few rows of the data
print(data)

# Save the data to a CSV file (optional)
data.to_csv(f"{ticker}_historical_data.csv")
