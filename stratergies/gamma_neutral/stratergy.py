# import math
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from binance_api import BinanceAPI
# from matplotlib.dates import DateFormatter

# class GammaNeutralCalendarSpread:
#     def __init__(self, symbol="BTCUSDT", api=None):
#         self.symbol = symbol
#         self.api = api or BinanceAPI()
#         self.history = []  # Store results for plotting later

#     def calculate_max_profit(self, long_leg_price, short_leg_price):
#         """Calculate the maximum profit from the strategy."""
#         return short_leg_price - long_leg_price

#     def calculate_max_loss(self, long_leg_price, short_leg_price):
#         """Calculate the maximum loss from the strategy."""
#         return  long_leg_price - short_leg_price

#     def calculate_apy(self, max_profit, max_loss, annualized_return,initial_investment=1000):
#         """Calculate the Annual Percentage Yield (APY) based on the profit and loss."""
#         try:
#             apy = ((max_profit - max_loss) / initial_investment) * annualized_return  # Ensures positive value for APY

#             return apy
#         except Exception as e:
#             print(f"Error calculating APY: {e}")
#             return None

#     def fetch_historical_data(self, interval="1d", start="1 Oct, 2024", end="today"):
#         """Fetch historical market data for the symbol."""
#         klines = self.api.get_historical_klines(self.symbol, interval, start, end)
#         df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_vol", "number_of_trades", "taker_buy_base_asset_vol", "taker_buy_quote_asset_vol", "ignore"])
#         df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
#         df["close"] = pd.to_numeric(df["close"])
#         return df

#     def simulate_trade(self):
#         """Simulate a Gamma Neutral Calendar Spread strategy based on fetched data."""
#         historical_data = self.fetch_historical_data()
#         # print('historical data , ', historical_data)

#         # Example: let's assume prices for long and short legs are calculated based on historical data
#         long_leg_price = historical_data["close"].iloc[-60]  # Price 60 days ago (long leg)
#         short_leg_price = historical_data["close"].iloc[-30]  # Price 30 days ago (short leg)

#         max_profit = self.calculate_max_profit(long_leg_price, short_leg_price)
#         max_loss = self.calculate_max_loss(long_leg_price, short_leg_price)
        
#         annualized_return = 0.12  # Example annualized return (12%)
#         apy = self.calculate_apy(max_profit, max_loss, annualized_return)

# # Add to history
#         # print all the values
#         # print apy
#         # print('apy , ', apy)
#         # print('btc price , ', historical_data["close"].iloc[-1])
#         # print('timestamp , ', historical_data["timestamp"].iloc[-1])
#         # print('max_profit , ', max_profit)
#         # print('max_loss , ', max_loss)
        
#         self.history.append({
#             "timestamp": historical_data["timestamp"].iloc[-1],  # Latest timestamp
#             "btc_price": historical_data["close"].iloc[-1],
#             "max_profit": max_profit,
#             "max_loss": max_loss,
#             "apy": apy
#         })

#     def get_history(self):
#         """Return the collected history as a DataFrame."""
#         return pd.DataFrame(self.history)
    
    


import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from binance_api import BinanceAPI
from matplotlib.dates import DateFormatter

class GammaNeutralCalendarSpread:
    def __init__(self, symbol="BTCUSDT", api=None):
        self.symbol = symbol
        self.api = api or BinanceAPI()
        self.history = []  # Store results for plotting later
        self.monthly_history = []  # Store monthly profit, loss, max profit, and loss

    def calculate_max_profit(self, long_leg_price, short_leg_price):
        """Calculate the maximum profit from the strategy."""
        return short_leg_price - long_leg_price

    def calculate_max_loss(self, long_leg_price, short_leg_price):
        """Calculate the maximum loss from the strategy."""
        return  long_leg_price - short_leg_price

    def calculate_apy(self, max_profit, max_loss, annualized_return, initial_investment=1000):
        """Calculate the Annual Percentage Yield (APY) based on the profit and loss."""
        try:
            apy = ((max_profit - max_loss) / initial_investment) * annualized_return  # Ensures positive value for APY
            return apy
        except Exception as e:
            print(f"Error calculating APY: {e}")
            return None

    def fetch_historical_data(self, interval="1d", start="1 Jan, 2023", end="today"):
        """Fetch historical market data for the symbol."""
        klines = self.api.get_historical_klines(self.symbol, interval, start, end)
        df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_vol", "number_of_trades", "taker_buy_base_asset_vol", "taker_buy_quote_asset_vol", "ignore"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close"] = pd.to_numeric(df["close"])
        df["month"] = df["timestamp"].dt.to_period("M")
        return df

    def simulate_trade(self):
            """Simulate a Gamma Neutral Calendar Spread strategy based on fetched data."""
            historical_data = self.fetch_historical_data()

            # Group data by month and calculate monthly stats
            monthly_data = historical_data.groupby("month").agg(
                start_price=("close", "first"),  # Price at the start of the month (long leg)
                end_price=("close", "last"),    # Price at the end of the month (short leg)
                avg_btc_price=("close", "mean")  # Average BTC price during the month
            )
            
            for month, row in monthly_data.iterrows():
                long_leg_price = row["start_price"]
                short_leg_price = row["end_price"]
                
                max_profit = self.calculate_max_profit(long_leg_price, short_leg_price)
                max_loss = self.calculate_max_loss(long_leg_price, short_leg_price)
                
                annualized_return = 0.12  # Example annualized return (12%)
                apy = self.calculate_apy(max_profit, max_loss, annualized_return)
                
                # Store monthly results, including avg BTC price
                self.monthly_history.append({
                    "month": month,
                    "max_profit": max_profit,
                    "max_loss": max_loss,
                    "apy": apy,
                    "monthly_profit_loss": short_leg_price - long_leg_price,  # Monthly profit/loss
                    "btc_price": row["avg_btc_price"]  # Avg BTC price
                })


    def get_monthly_history(self):
        """Return the monthly history as a DataFrame."""
        return pd.DataFrame(self.monthly_history)

    def plot_monthly_performance(self):
        """BTC-USDT Monthly Performance."""
        monthly_df = self.get_monthly_history()
        

        # Create a figure with subplots (3 rows x 2 columns)
        fig, axes = plt.subplots(3, 2, figsize=(16, 12), constrained_layout=True)

        # BTC Price over time
        axes[0, 0].plot(monthly_df["month"].astype(str), monthly_df["btc_price"], label="BTC Price", marker='o', color='orange')
        axes[0, 0].set_title("Avg BTC Price Over Time")
        axes[0, 0].set_xlabel("Month")
        axes[0, 0].set_ylabel("BTC Price (USDT)")
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].legend()

        # Combined Max Profit and Max Loss
        axes[0, 1].plot(monthly_df["month"].astype(str), monthly_df["max_profit"], label="Max Profit", marker='o', color='green')
        axes[0, 1].plot(monthly_df["month"].astype(str), monthly_df["max_loss"], label="Max Loss", marker='o', color='red')
        axes[0, 1].set_title("Max Profit and Max Loss Over Months")
        axes[0, 1].set_xlabel("Month")
        axes[0, 1].set_ylabel("Value (USDT)")
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].legend()

        # Monthly Profit/Loss as bar graph
        axes[1, 0].bar(monthly_df["month"].astype(str), monthly_df["monthly_profit_loss"], color='blue', alpha=0.7)
        axes[1, 0].set_title("Avg Monthly Profit/Loss")
        axes[1, 0].set_xlabel("Month")
        axes[1, 0].set_ylabel("Profit/Loss (USDT)")
        axes[1, 0].tick_params(axis='x', rotation=45)

        # APY over time
        axes[1, 1].plot(monthly_df["month"].astype(str), monthly_df["apy"], label="APY", marker='o', color='purple')
        axes[1, 1].set_title("APY Over Months")
        axes[1, 1].set_xlabel("Month")
        axes[1, 1].set_ylabel("APY (%)")
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].legend()

        # Empty Subplot for better alignment
        fig.delaxes(axes[2, 0])  # Remove extra subplot if there's an odd number of plots
        fig.delaxes(axes[2, 1])  # Remove extra subplot

        # Add overall title
        # Add overall title at the top of the plot
        plt.suptitle("BTC-USDT Gamma Neutral Calendar Spread - Monthly Performance", fontsize=20, y=1.03, fontweight='bold')

        # Show plot
        plt.show()



# Usage Example:
# Create an instance of the strategy class
strategy = GammaNeutralCalendarSpread()

# Simulate trades and calculate monthly performance
strategy.simulate_trade()

# Retrieve and print the monthly history (max profit, max loss, APY, etc.)
monthly_history = strategy.get_monthly_history()
print(monthly_history)

# Plot the monthly performance
strategy.plot_monthly_performance()
