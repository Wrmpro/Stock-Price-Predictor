

# 📈 Stock Price Predictor & Visualization App

An end-to-end project that combines **Machine Learning-based stock price prediction** with an **interactive Streamlit dashboard** for visualization and analysis.

This project allows you to:

* Train ML models on historical stock data
* Predict future stock prices
* Explore real-time stock and index data (US + Indian markets)
* Visualize trends, statistics, and volumes interactively

---

## 🚀 Features

- ✅ **Historical Data Training** – Linear Regression (extendable to LSTM, XGBoost, etc.)
- ✅ **Interactive Streamlit Dashboard** – View stock charts and stats
- ✅ **Supports US & Indian Stocks** (AAPL, TSLA, RELIANCE.NS, TCS.NS, etc.)
- ✅ **Indices Support** – NIFTY 50 (^NSEI), SENSEX (^BSESN)
- 📊 **Closing price trends**, 📌 **Stock statistics**, 📉 **Trading volume**

---

## 🔑 Example Stock Symbols

* **US Stocks:** `AAPL`, `TSLA`, `MSFT`
* **Indian Stocks:** `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`
* **Indices:** `^NSEI` (NIFTY 50), `^BSESN` (SENSEX)

👉 For Indian stocks, add `.NS` at the end (e.g., `INFY.NS`)

---

## 🛠️ Tech Stack

* **Python 3**
* **Streamlit** – dashboard & visualization
* **yfinance** – stock market data
* **scikit-learn** – ML models (Linear Regression)
* **pandas, numpy** – data handling
* **matplotlib** – visualization

---

## 📂 Project Structure

```
📦 stock-price-predictor
 ┣ 📜 README.md             # Documentation
 ┣ 📜 requirements.txt      # Dependencies
 ┣ 📜 setup.py              # Setup file
 ┣ 📜 app.py                # Streamlit app (visualization dashboard)
 ┣ 📂 src/                  # ML prediction pipeline
 ┃ ┣ 📜 main.py             # Entry point for ML model training/prediction
 ┃ ┗ 📂 spp/
 ┃   ┣ 📜 __init__.py
 ┃   ┣ 📜 data_loader.py    # Fetches and preprocesses stock data
 ┃   ┣ 📜 model.py          # ML model (Linear Regression, extendable)
 ┃   ┗ 📜 utils.py          # Helper functions
```

---

## 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/stock-price-predictor.git
   cd stock-price-predictor
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### 🧠 Run the ML Predictor

```bash
python src/main.py
```

### 🌐 Run the Streamlit Dashboard

```bash
streamlit run app.py
```

---

## 🌐 Live Demo

👉 [Try the Streamlit App](https://your-app-link.streamlit.app)

---

## 💡 Future Enhancements

* Add **deep learning models (LSTM, GRU, Prophet)**
* Add **real-time stock prediction**
* Add **portfolio tracking & alerts**
* Integrate **news sentiment analysis**

---

## 👨‍💻 Author

**Shashank N**

> Aspiring Software Engineer | AI-ML Enthusiast | Passionate about building impactful projects

---

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This project is licensed under the **MIT License**.

---

