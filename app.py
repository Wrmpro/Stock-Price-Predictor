import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Stock Price App", page_icon="📈", layout="wide")

st.title("📈 Stock Price Visualization App")

# Sidebar for user input
st.sidebar.header("Stock Selection")

# Stock symbol input
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT):", "AAPL")

# Date range input
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Fetch data
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    return data

if ticker_symbol:
    try:
        data = load_data(ticker_symbol, start_date, end_date)

        st.subheader(f"Showing data for {ticker_symbol}")
        st.write(data.tail())

        # Line chart
        st.line_chart(data.set_index("Date")["Close"], use_container_width=True)

        # Extra info
        st.subheader("Stock Statistics")
        st.metric("Latest Closing Price", f"${data['Close'].iloc[-1]:.2f}")
        st.metric("Highest Price", f"${data['High'].max():.2f}")
        st.metric("Lowest Price", f"${data['Low'].min():.2f}")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

