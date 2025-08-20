import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Page config
st.set_page_config(page_title="Stock Price App", page_icon="📈", layout="wide")

st.title("📈 Stock Price Visualization App")

# Sidebar for user input
st.sidebar.header("Stock Selection")

st.sidebar.markdown(
    """
    ✅ **Examples**  
    - US Stocks: `AAPL`, `TSLA`, `MSFT`  
    - Indian Stocks: `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`
    """
)

# Stock symbol input
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol:", "AAPL")

# Date range input
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Function to fetch stock data
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    return data

if ticker_symbol:
    try:
        # Load data
        data = load_data(ticker_symbol, start_date, end_date)

        # Show recent data
        st.subheader(f"📌 Showing data for **{ticker_symbol}**")
        st.dataframe(data.tail(), use_container_width=True)

        # Line chart (Closing price)
        st.subheader("📊 Closing Price Over Time")
        st.line_chart(data.set_index("Date")["Close"], use_container_width=True)

        # Extra info
        st.subheader("📌 Stock Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Closing Price", f"₹{data['Close'].iloc[-1]:.2f}" if ticker_symbol.endswith(".NS") else f"${data['Close'].iloc[-1]:.2f}")
        col2.metric("Highest Price", f"₹{data['High'].max():.2f}" if ticker_symbol.endswith(".NS") else f"${data['High'].max():.2f}")
        col3.metric("Lowest Price", f"₹{data['Low'].min():.2f}" if ticker_symbol.endswith(".NS") else f"${data['Low'].min():.2f}")

        # Optional: Volume chart
        st.subheader("📊 Trading Volume")
        st.bar_chart(data.set_index("Date")["Volume"], use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")
