import yfinance as yf
import matplotlib.pyplot as plt

ticker = "AAPL"
stock = yf.Ticker(ticker)
data = stock.history(period="6mo")

# Calculate moving averages
data["20 Day MA"] = data["Close"].rolling(window=20).mean()
data["50 Day MA"] = data["Close"].rolling(window=50).mean()

# Plot closing price with both moving averages
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="Close Price", linewidth=1.5)
plt.plot(data.index, data["20 Day MA"], label="20-Day MA", linewidth=1.5)
plt.plot(data.index, data["50 Day MA"], label="50-Day MA", linewidth=1.5)

plt.title(f"{ticker} Stock Price with Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("stock_chart.png")
plt.show()