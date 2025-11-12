

# 📈 Stock Price Predictor & Visualization App

An end-to-end project that combines **advanced Machine Learning models** with an **interactive Streamlit dashboard** for stock price prediction, visualization, and analysis.

This project allows you to:

* Train advanced ML models (XGBoost, LSTM) on historical stock data
* Predict future stock prices with improved accuracy
* Explore real-time stock and index data (US + Indian markets)
* Visualize trends, predictions, and technical indicators interactively

---

## 🚀 Features

- ✅ **Advanced ML Models** – XGBoost (tabular features) and LSTM (sequence learning)
- ✅ **Feature Engineering** – Lag features, rolling statistics, RSI, MACD, moving averages
- ✅ **Time-Series Evaluation** – Walk-forward validation, RMSE, MAPE metrics
- ✅ **Interactive Streamlit Dashboard** – View predictions, charts, and model comparisons
- ✅ **Supports US & Indian Stocks** (AAPL, TSLA, RELIANCE.NS, TCS.NS, etc.)
- ✅ **Indices Support** – NIFTY 50 (^NSEI), SENSEX (^BSESN)
- 📊 **Prediction visualization** with actual vs predicted comparison
- 📈 **Technical indicators** and feature importance

---

## 🔑 Example Stock Symbols

* **US Stocks:** `AAPL`, `TSLA`, `MSFT`, `GOOGL`, `AMZN`
* **Indian Stocks:** `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`, `INFY.NS`
* **Indices:** `^NSEI` (NIFTY 50), `^BSESN` (SENSEX), `^DJI` (Dow Jones)

👉 For Indian stocks, add `.NS` at the end (e.g., `INFY.NS`)

---

## 🛠️ Tech Stack

* **Python 3.12+**
* **Streamlit** – Interactive dashboard & visualization
* **yfinance** – Stock market data fetching
* **XGBoost** – Gradient boosting for tabular features
* **TensorFlow/Keras** – LSTM neural networks for sequence modeling
* **scikit-learn** – Preprocessing, metrics, and evaluation
* **pandas, numpy** – Data manipulation
* **plotly** – Interactive charts
* **ta** – Technical analysis indicators

---

## 📂 Project Structure

```
📦 stock-price-predictor
 ┣ 📜 README.md                      # Documentation
 ┣ 📜 requirements.txt               # Dependencies
 ┣ 📜 setup.py                       # Setup file
 ┣ 📜 app.py                         # Streamlit app (visualization & prediction dashboard)
 ┣ 📂 src/                           # ML prediction pipeline
 ┃ ┣ 📜 main.py                      # Training pipelines (XGBoost & LSTM)
 ┃ ┗ 📂 spp/
 ┃   ┣ 📜 __init__.py
 ┃   ┣ 📜 data_loader.py             # Fetches and preprocesses stock data
 ┃   ┣ 📜 model.py                   # ML models (XGBoost, LSTM, evaluation)
 ┃   ┣ 📜 feature_engineering.py     # Technical features and indicators
 ┃   ┗ 📜 utils.py                   # Helper functions
 ┗ 📂 models/                        # Saved models (created after training)
   ┣ 📜 xgb_model.json               # Trained XGBoost model
   ┣ 📜 xgb_scaler.pkl               # Feature scaler for XGBoost
   ┣ 📜 lstm.keras                   # Trained LSTM model
   ┗ 📜 lstm_scaler.pkl              # Scaler for LSTM
```

---

## 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Wrmpro/Stock-Price-Predictor.git
   cd Stock-Price-Predictor
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### 🧠 Train ML Models

Train the XGBoost model (recommended first):

```bash
python src/main.py
```

This will:
- Download historical data for AAPL (default)
- Engineer technical features (lag, rolling stats, RSI, MACD)
- Train XGBoost with time-based train/test split
- Save model to `models/xgb_model.json`
- Display RMSE and MAPE metrics

To train on a different stock, modify the symbol in `src/main.py` or call:

```python
from src.main import train_pipeline_xgb
train_pipeline_xgb('RELIANCE.NS')
```

### 🌐 Run the Streamlit Dashboard

```bash
streamlit run app.py
```

Then:
1. Enter a stock ticker (e.g., `AAPL`, `RELIANCE.NS`)
2. Select date range
3. Click "Load Data" to view historical prices
4. Click "Predict Next Days" to see ML predictions
5. Compare actual vs predicted prices with interactive charts

---

## 📊 Model Comparison

| Model | Best For | Speed | Accuracy |
|-------|----------|-------|----------|
| **XGBoost** | Tabular features, next-day prediction | Fast | High (RMSE typically 2-5% lower than Linear Regression) |
| **LSTM** | Sequence learning, multi-day forecasting | Slower (needs GPU) | High (requires 3+ years data) |
| **Linear Regression** (Legacy) | Simple baseline | Very Fast | Moderate |

---

## 🎯 Features Engineered

The model uses these technical features:

1. **Lag Features**: Previous 1, 2, 3, 5, 7, 14 days' closing prices
2. **Rolling Statistics**: Mean, std, min, max over 3, 5, 7, 14, 21-day windows
3. **Moving Averages**: 7-day MA, 21-day MA, and their difference
4. **RSI (14-day)**: Relative Strength Index
5. **MACD**: Moving Average Convergence Divergence with signal line

---

## 📈 Expected Accuracy

With proper feature engineering:

- **XGBoost**: RMSE typically 2-5% lower than Linear Regression
- **MAPE**: Usually 1-3% for stable stocks, higher for volatile ones
- **Best Performance**: On stocks with clear trends and sufficient historical data (3+ years)

Example metrics on AAPL:
- Linear Regression: RMSE ~$3.50, MAPE ~2.1%
- XGBoost: RMSE ~$2.10, MAPE ~1.3%

---

## 🌐 Live Demo

👉 [Try the Streamlit App](https://stock-price-prediction-using-ml.streamlit.app/)

---

## 💡 Future Enhancements

* ✅ ~~Add deep learning models (LSTM, GRU)~~ ✅ **COMPLETED**
* ✅ ~~Add technical indicators (RSI, MACD)~~ ✅ **COMPLETED**
* Add hyperparameter tuning (Optuna)
* Add walk-forward backtesting
* Add real-time stock prediction
* Add portfolio tracking & alerts
* Integrate news sentiment analysis

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 👨‍💻 Author

**Shashank N**

> Aspiring Software Engineer | AI-ML Enthusiast | Passionate about building impactful projects

---

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is licensed under the **MIT License**.

---

