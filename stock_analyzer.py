import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    """Fetch 6 months of price history and calculate moving averages for one stock."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="6mo")
    data["20 Day MA"] = data["Close"].rolling(window=20).mean()
    data["50 Day MA"] = data["Close"].rolling(window=50).mean()
    return data

# List of tickers to analyze
tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]

# Dictionary to store each stock's data, keyed by ticker symbol
all_data = {}

for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    all_data[ticker] = get_stock_data(ticker)

print("\nDone. Data fetched for:", list(all_data.keys()))