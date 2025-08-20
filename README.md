📈 Stock Price Predictor

A machine learning project that predicts stock prices using historical data.
Currently implemented with Linear Regression, but extendable with advanced models such as LSTM, GRU, XGBoost, etc.

🚀 Features

✅ Fetches stock data using yFinance
✅ Trains a regression model on historical data
✅ Predicts future stock prices
✅ Visualizes results with Matplotlib & Streamlit
✅ Clean and interactive web UI

🛠 Tech Stack

Python 3

NumPy, Pandas → Data handling

Scikit-learn → Machine Learning

Matplotlib → Visualization

yFinance → Stock data

Streamlit → Web app deployment

🔧 Installation

Clone the repository

git clone https://github.com/your-username/stock-price-predictor.git
cd stock-price-predictor


Install dependencies

pip install -r requirements.txt


Run the Streamlit app

streamlit run app.py


Open http://localhost:8501
 in your browser.

📂 Project Structure
stock-price-predictor/
│── README.md
│── requirements.txt
│── setup.py
│── app.py
│── src/
│   ├── main.py
│   └── spp/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── model.py
│       └── utils.py

## Live App

👉[Try the app here](https://stock-price-prediction-using-ml.streamlit.app/)


🖥 Example Screenshots

📊 Closing Price Trend
📊 Predicted vs Actual Prices

(You can add screenshots of your Streamlit app here once deployed.)

💡 Future Enhancements

Add deep learning models (LSTM, GRU)

Use real-time stock data APIs

Deploy using Flask/Django or FastAPI

Integrate database for saving predictions

Add moving averages & technical indicators

👨‍💻 Author

Shashank N

Aspiring Software Engineer | AI-ML Enthusiast | Passionate about building impactful projects

📄 License

This project is licensed under the MIT License.
