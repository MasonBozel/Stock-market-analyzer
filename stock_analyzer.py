import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)
data = stock.history(period="6mo")

# Calculate a 20-day moving average of the closing price
data["20 Day MA"] = data["Close"].rolling(window=20).mean()

print(data[["Close", "20 Day MA"]].tail(10))