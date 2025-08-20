
# Stock Price Predictor

This project predicts stock prices using historical data with machine learning techniques.  
It uses **Linear Regression** and can be extended with advanced models (LSTM, XGBoost, etc.).

## Features
- Fetches stock data using **yfinance**
- Trains a regression model on historical data
- Predicts future stock prices
- Visualizes results with matplotlib

## Tech Stack
- Python 3
- NumPy, Pandas (data handling)
- Scikit-learn (ML)
- Matplotlib (visualization)
- yFinance (stock data)

## Installation
```bash
git clone https://github.com/your-username/stock-price-predictor.git
cd stock-price-predictor
pip install -r requirements.txt
```

## Usage
```bash
python src/main.py
```

## Project Structure
```
stock-price-predictor/
│── README.md
│── requirements.txt
│── setup.py
│── src/
│   ├── main.py
│   └── spp/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── model.py
│       └── utils.py
```

## Future Enhancements
- Add deep learning models (LSTM, GRU)
- Use real-time stock data APIs
- Deploy using Flask/Django
