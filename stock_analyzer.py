import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)
data = stock.history(period="6mo")

print("Data shape:", data.shape)
print("Is empty?", data.empty)
print(data.head())