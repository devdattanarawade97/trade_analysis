import matplotlib.pyplot as plt

from stratergy import GammaNeutralCalendarSpread

def plot_gamma_neutral_results(strategy):
    # Get the historical data (history of simulations)
    df = strategy.get_history()

    # Ensure the timestamp is the index for plotting
    df.set_index("timestamp", inplace=True)

    # Plot BTC Price Over Time
    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.plot(df.index, df["btc_price"], label="BTC Price", color="blue")
    plt.title("BTC Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USDT)")
    plt.xticks(rotation=45)

    # Plot Max Profit Over Time
    plt.subplot(2, 2, 2)
    plt.plot(df.index, df["max_profit"], label="Max Profit", color="green")
    plt.title("Max Profit Over Time")
    plt.xlabel("Date")
    plt.ylabel("Max Profit (USDT)")
    plt.xticks(rotation=45)

    # Plot Max Loss Over Time
    plt.subplot(2, 2, 3)
    plt.plot(df.index, df["max_loss"], label="Max Loss", color="red")
    plt.title("Max Loss Over Time")
    plt.xlabel("Date")
    plt.ylabel("Max Loss (USDT)")
    plt.xticks(rotation=45)

    # Plot APY Over Time
    plt.subplot(2, 2, 4)
    plt.plot(df.index, df["apy"], label="APY", color="purple")
    plt.title("APY Over Time")
    plt.xlabel("Date")
    plt.ylabel("APY (%)")
    plt.xticks(rotation=45)

    # Improve layout and show the plot
    plt.tight_layout()
    plt.show()

# Example usage
# Create an instance of the strategy
strategy = GammaNeutralCalendarSpread(symbol="BTCUSDT")

# Simulate trades (can call this multiple times or for a specific date range)
for _ in range(30):  # Simulate 30 days of trades (adjust as necessary)
    strategy.simulate_trade()

# Plot the results
plot_gamma_neutral_results(strategy)
