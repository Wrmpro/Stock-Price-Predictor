
import yfinance as yf

def load_data(ticker="AAPL", period="6mo", interval="1d"):
    return yf.download(ticker, period=period, interval=interval)
