import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Page config
st.set_page_config(page_title="Stock & Index Tracker", page_icon="📈", layout="wide")

st.title("📈 Stock & Index Visualization App")

# Sidebar for user input
st.sidebar.header("Stock / Index Selection")

st.sidebar.markdown(
    """
    ✅ **Examples**  
    - US Stocks: `AAPL`, `TSLA`, `MSFT`  
    - Indian Stocks: `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`  
    - Indices: `NIFTY 50`, `SENSEX`
    """
)

# Dropdown for popular Indian indices
index_options = {
    "NIFTY 50": "^NSEI",
    "SENSEX (BSE 30)": "^BSESN"
}
selected_index = st.sidebar.selectbox("Choose Index (Optional)", ["None"] + list(index_options.keys()))

# Stock symbol input (overrides index if entered)
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol:", "")

# Date range input
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Decide ticker
if ticker_symbol.strip():
    ticker = ticker_symbol.strip().upper()
elif selected_index != "None":
    ticker = index_options[selected_index]
else:
    ticker = "AAPL"  # default

# Function to fetch stock data
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    return data

if ticker:
    try:
        # Load data
        data = load_data(ticker, start_date, end_date)

        if data.empty:
            st.error("⚠️ No data found! Check symbol or date range.")
        else:
            # Show recent data
            st.subheader(f"📌 Showing data for **{ticker}**")
            st.dataframe(data.tail(), use_container_width=True)

            # Line chart (Closing price)
            st.subheader("📊 Closing Price Over Time")
            st.line_chart(data.set_index("Date")["Close"], use_container_width=True)

            # Extra info
            st.subheader("📌 Stock Statistics")
            col1, col2, col3 = st.columns(3)

            currency = "₹" if ticker.endswith(".NS") or ticker in index_options.values() else "$"
            col1.metric("Latest Closing Price", f"{currency}{data['Close'].iloc[-1]:.2f}")
            col2.metric("Highest Price", f"{currency}{data['High'].max():.2f}")
            col3.metric("Lowest Price", f"{currency}{data['Low'].min():.2f}")

            # Optional: Volume chart (not all indices have volume)
            if "Volume" in data.columns:
                st.subheader("📊 Trading Volume")
                st.bar_chart(data.set_index("Date")["Volume"], use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")
