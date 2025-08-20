import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# --- Page config ---
st.set_page_config(page_title="Stock & Index Tracker", page_icon="📈", layout="wide")
st.title("📈 Stock & Index Visualization App")

# --- Sidebar inputs ---
st.sidebar.header("Stock / Index Selection")
st.sidebar.markdown("""
✅ **Examples**  
- US Stocks: `AAPL`, `TSLA`, `MSFT`  
- Indian Stocks: `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`  
- Indices: `NIFTY 50 - ^NSEI`, `SENSEX - ^BSESN`
""")

# Popular Indian indices
index_options = {"NIFTY 50": "^NSEI", "SENSEX (BSE 30)": "^BSESN"}
selected_index = st.sidebar.selectbox("Choose Index (Optional)", ["None"] + list(index_options.keys()))

# Stock symbol input (overrides index if entered)
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol:", "")

# Date range
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# --- Quick Example Buttons ---
st.markdown("### ✅ Quick Examples")
cols = st.columns(8)
examples = ["AAPL", "TSLA", "MSFT", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "^NSEI", "^BSESN"]
for col, sym in zip(cols, examples):
    if col.button(sym.replace("^NSEI", "NIFTY 50").replace("^BSESN", "SENSEX")):
        ticker_symbol = sym

# --- Decide final ticker safely ---
ticker_symbol = str(ticker_symbol)
if ticker_symbol.strip() != "":
    ticker = ticker_symbol.strip().upper()
elif selected_index != "None":
    ticker = index_options[selected_index]
else:
    ticker = "AAPL"

# --- Load data function ---
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end, progress=False)
    data.reset_index(inplace=True)
    return data

# --- Main Section ---
try:
    data = load_data(ticker, start_date, end_date)

    if data.empty:
        st.error("⚠️ No data found! Check symbol or date range.")
    else:
        # Show recent data
        st.subheader(f"📌 Showing data for **{ticker}**")
        st.dataframe(data.tail(), use_container_width=True)

        # Closing price chart
        st.subheader("📊 Closing Price Over Time")
        st.line_chart(data.set_index("Date")["Close"], use_container_width=True)

        # Stock Statistics
        st.subheader("📌 Stock Statistics")
        col1, col2, col3 = st.columns(3)

        currency = "₹" if ticker.endswith(".NS") or ticker in ["^NSEI", "^BSESN"] else "$"
        latest_close = float(data['Close'].iloc[-1])
        highest_price = float(data['High'].max())
        lowest_price = float(data['Low'].min())

        col1.metric("Latest Closing Price", f"{currency}{latest_close:.2f}")
        col2.metric("Highest Price", f"{currency}{highest_price:.2f}")
        col3.metric("Lowest Price", f"{currency}{lowest_price:.2f}")

        # Volume chart
        if "Volume" in data.columns and data["Volume"].sum() > 0:
            st.subheader("📊 Trading Volume")
            st.bar_chart(data.set_index("Date")["Volume"], use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error fetching data: {e}")
