from binance.client import Client
import os
class BinanceAPI:
    def __init__(self):
        self.api_key = os.environ.get("BINANCE_API_KEY")
        self.secret_key = os.environ.get("BINANCE_API_SECRET")
   
        self.client = Client(api_key=self.api_key, api_secret=self.secret_key)

    def get_account_info(self):
        """Fetches account information."""
        try:
            return self.client.get_account()
        except Exception as e:
            print(f"Error fetching account info: {e}")
            return None

    def get_symbol_ticker(self, symbol):
        """Fetches current ticker price for a given symbol."""
        try:
            return self.client.get_symbol_ticker(symbol=symbol)
        except Exception as e:
            print(f"Error fetching ticker price for {symbol}: {e}")
            return None

    def get_historical_klines(self, symbol, interval, start_str, end_str=None):
        """
        Fetches historical kline (candlestick) data.
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT').
            interval (str): Kline interval (e.g., '1d', '1h').
            start_str (str): Start date (e.g., '1 Jan, 2021').
            end_str (str): End date (optional).
        Returns:
            List of klines.
        """
        try:
            return self.client.get_historical_klines(symbol, interval, start_str, end_str)
        except Exception as e:
            print(f"Error fetching historical klines: {e}")
            return None

# Example usage
if __name__ == "__main__":
    api = BinanceAPI()
    ticker = api.get_symbol_ticker(symbol="BTCUSDT")
    print("BTC Price:", ticker)
