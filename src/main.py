
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from spp.model import train_model, predict_prices

def main():
    ticker = "AAPL"
    print(f"Downloading stock data for {ticker}...")
    data = yf.download(ticker, period="6mo", interval="1d")

    if data.empty:
        print("No data found. Check ticker symbol.")
        return

    print("Training model...")
    model, X_test, y_test = train_model(data)

    print("Predicting future prices...")
    predictions = predict_prices(model, X_test)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.values, label="Actual")
    plt.plot(predictions, label="Predicted")
    plt.legend()
    plt.title(f"Stock Price Prediction for {ticker}")
    plt.show()

if __name__ == "__main__":
    main()

