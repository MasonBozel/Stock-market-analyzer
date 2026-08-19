import yfinance as yf
import matplotlib.pyplot as plt
import sqlite3

def get_stock_data(ticker):
    """Fetch 6 months of price history and calculate moving averages and returns for one stock."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="6mo")
    data["20 Day MA"] = data["Close"].rolling(window=20).mean()
    data["50 Day MA"] = data["Close"].rolling(window=50).mean()
    data["Daily Return"] = data["Close"].pct_change()
    return data

def backtest_crossover_strategy(data):
    """Simulate a moving average crossover strategy and compare to buy-and-hold."""
    data["Signal"] = (data["20 Day MA"] > data["50 Day MA"]).astype(int)
    data["Position"] = data["Signal"].shift(1)
    data["Strategy Return"] = data["Daily Return"] * data["Position"]
    strategy_total_return = (1 + data["Strategy Return"]).prod() - 1
    buy_hold_total_return = (1 + data["Daily Return"]).prod() - 1
    return strategy_total_return * 100, buy_hold_total_return * 100

def plot_stock_prices(all_data):
    """Plot closing prices for all stocks on one chart for comparison."""
    plt.figure(figsize=(12, 6))
    for ticker, data in all_data.items():
        plt.plot(data.index, data["Close"], label=ticker, linewidth=1.5)

    plt.title("Stock Price Comparison (6 Months)")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("stock_chart.png")
    plt.show()

def store_data_in_db(all_data, db_name="stock_data.db"):
    """Store all stocks' price data into a SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the table if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            ticker TEXT,
            date TEXT,
            close REAL,
            daily_return REAL,
            ma_20 REAL,
            ma_50 REAL
        )
    """)

    # Clear old data first so re-running the script doesn't create duplicates
    cursor.execute("DELETE FROM stock_prices")

    # Insert each row of each stock's data into the table
    for ticker, data in all_data.items():
        for date, row in data.iterrows():
            cursor.execute("""
                INSERT INTO stock_prices (ticker, date, close, daily_return, ma_20, ma_50)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ticker, str(date.date()), row["Close"], row["Daily Return"], row["20 Day MA"], row["50 Day MA"]))

    conn.commit()
    conn.close()
    print("\nData successfully stored in stock_data.db")

def query_average_close(db_name="stock_data.db"):
    """Query the database for each stock's average closing price."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ticker, AVG(close) as avg_close
        FROM stock_prices
        GROUP BY ticker
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# List of tickers to analyze
tickers = ["AAPL", "MSFT", "TSLA", "GOOGL"]

# Dictionary to store each stock's data, keyed by ticker symbol
all_data = {}

for ticker in tickers:
    print(f"Fetching data for {ticker}...")
    all_data[ticker] = get_stock_data(ticker)

print("\nDone. Data fetched for:", list(all_data.keys()))

# Approximate annual risk-free rate (based on recent short-term Treasury yields)
risk_free_rate = 0.045
risk_free_daily = risk_free_rate / 252

print("\n--- 6-Month Performance Comparison ---")
for ticker, data in all_data.items():
    total_return = (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1) * 100
    daily_volatility = data["Daily Return"].std()
    volatility = daily_volatility * 100
    avg_daily_return = data["Daily Return"].mean()
    sharpe_ratio = (avg_daily_return - risk_free_daily) / daily_volatility
    print(f"{ticker}: Total Return = {total_return:.2f}%, Daily Volatility = {volatility:.2f}%, Sharpe Ratio = {sharpe_ratio:.3f}")

print("\n--- Backtest: Moving Average Crossover Strategy vs. Buy & Hold ---")
for ticker, data in all_data.items():
    strategy_return, buy_hold_return = backtest_crossover_strategy(data)
    print(f"{ticker}: Strategy Return = {strategy_return:.2f}%, Buy & Hold Return = {buy_hold_return:.2f}%")

# Store everything in a SQL database
store_data_in_db(all_data)

# Query the database to confirm it worked
print("\n--- SQL Query: Average Closing Price by Ticker ---")
for ticker, avg_close in query_average_close():
    print(f"{ticker}: ${avg_close:.2f}")

# Plot all stocks for visual comparison
plot_stock_prices(all_data)