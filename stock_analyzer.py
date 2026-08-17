import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    """Fetch 6 months of price history and calculate moving averages and returns for one stock."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="6mo")
    data["20 Day MA"] = data["Close"].rolling(window=20).mean()
    data["50 Day MA"] = data["Close"].rolling(window=50).mean()
    data["Daily Return"] = data["Close"].pct_change()
    return data

# List of tickers to analyze
tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]

# Dictionary to store each stock's data, keyed by ticker symbol
all_data = {}

for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    all_data[ticker] = get_stock_data(ticker)

print("\nDone. Data fetched for:", list(all_data.keys()))

# Approximate annual risk-free rate (based on recent short-term Treasury yields)
risk_free_rate = 0.045  # 4.5%
risk_free_daily = risk_free_rate / 252  # 252 trading days in a year

# Compare returns, volatility, and risk-adjusted performance across all stocks
print("\n--- 6-Month Performance Comparison ---")
for ticker, data in all_data.items():
    total_return = (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100
    daily_volatility = data["Daily Return"].std()
    volatility = daily_volatility * 100

    avg_daily_return = data["Daily Return"].mean()
    sharpe_ratio = (avg_daily_return - risk_free_daily) / daily_volatility

    print(f"{ticker}: Total Return = {total_return:.2f}%, Daily Volatility = {volatility:.2f}%, Sharpe Ratio = {sharpe_ratio:.3f}")