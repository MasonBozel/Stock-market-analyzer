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

def backtest_crossover_strategy(data):
    """Simulate a moving average crossover strategy and compare to buy and hold."""
    # Signal: 1 if short-term MA is above long-term MA (bullish), else 0
    data["Signal"] = (data["20 Day MA"] > data["50 Day MA"]).astype(int)

    # Shift signal forward by 1 day - we can only act on yesterday's signal, not today's
    data["Position"] = data["Signal"].shift(1)

    # Strategy return: only earn the day's return when we hold a position
    data["Strategy Return"] = data["Daily Return"] * data["Position"]

    # Compare cumulative growth: strategy vs. buy and hold
    strategy_total_return = (1 + data["Strategy Return"]).prod() - 1
    buy_hold_total_return = (1 + data["Daily Return"]).prod() - 1

    return strategy_total_return * 100, buy_hold_total_return * 100

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

# Backtest the crossover strategy against buy and hold
print("\n--- Backtest: Moving Average Crossover Strategy vs. Buy & Hold ---")
for ticker, data in all_data.items():
    strategy_return, buy_hold_return = backtest_crossover_strategy(data)
    print(f"{ticker}: Strategy Return = {strategy_return:.2f}%, Buy & Hold Return = {buy_hold_return:.2f}%")