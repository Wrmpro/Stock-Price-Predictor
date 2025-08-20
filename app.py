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
    - Indices: `NIFTY 50 - ^NSEI`, `SENSEX - ^BSESN`
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

# --- Example Quick Buttons Section ---
st.markdown("### ✅ Quick Examples")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("AAPL (Apple)"):
        ticker_symbol = "AAPL"
with col2:
    if st.button("TSLA (Tesla)"):
        ticker_symbol = "TSLA"
with col3:
    if st.button("MSFT (Microsoft)"):
        ticker_symbol = "MSFT"

col4, col5, col6 = st.columns(3)
with col4:
    if st.button("RELIANCE.NS"):
        ticker_symbol = "RELIANCE.NS"
with col5:
    if st.button("TCS.NS"):
        ticker_symbol = "TCS.NS"
with col6:
    if st.button("HDFCBANK.NS"):
        ticker_symbol = "HDFCBANK.NS"

col7, col8 = st.columns(2)
with col7:
    if st.button("NIFTY 50"):
        ticker_symbol = "^NSEI"
with col8:
    if st.button("SENSEX"):
        ticker_symbol = "^BSESN"

# --- Decide final ticker ---
if ticker_symbol.strip():
    ticker = str(ticker_symbol.strip().upper())
elif selected_index != "None":
    ticker = str(index_options[selected_index])
else:
    ticker = "AAPL"  # default


# Helpers to normalize yfinance columns
def _get_column_as_series(df: pd.DataFrame, col_name: str) -> pd.Series:
    """
    Return the requested column as a 1-D Series, even if df[col_name] is a DataFrame
    (e.g., from multi-index columns). If multiple subcolumns exist, take the first.
    """
    col = df[col_name]
    if isinstance(col, pd.DataFrame):
        # Reduce to first sub-column if multi-dimensional
        col = col.iloc[:, 0]
    # Ensure numeric if possible
    col = pd.to_numeric(col, errors="coerce")
    return col


# Function to fetch stock data
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)
    return data

# --- Main Section ---
if ticker:
    try:
        # Validate date range early
        if start_date > end_date:
            st.error("⚠️ Start Date must be before End Date.")
        else:
            # Load data
            data = load_data(ticker, start_date, end_date)

            if data.empty:
                st.error("⚠️ No data found! Check symbol or date range.")
            else:
                # Show recent data
                st.subheader(f"📌 Showing data for **{ticker}**")
                st.dataframe(data.tail(), use_container_width=True)

                # Prepare Close series safely for chart
                if "Close" in data.columns:
                    close_ser = _get_column_as_series(data, "Close")
                    close_plot = pd.DataFrame({"Close": close_ser.values}, index=data["Date"])
                    st.subheader("📊 Closing Price Over Time")
                    st.line_chart(close_plot["Close"], use_container_width=True)

                # Stock Statistics
                st.subheader("📌 Stock Statistics")
                col1, col2, col3 = st.columns(3)
                
                # Detect currency (₹ for Indian stocks/indices, $ for US)
                if ticker.endswith(".NS") or ticker in ["^NSEI", "^BSESN"]:
                    currency = "₹"
                else:
                    currency = "$"
                
                # Safely compute metrics
                # Close
                if "Close" in data.columns:
                    close_ser = _get_column_as_series(data, "Close")
                    latest_close_val = float(close_ser.iloc[-1])
                else:
                    latest_close_val = float("nan")

                # High
                if "High" in data.columns:
                    high_ser = _get_column_as_series(data, "High")
                    highest_price_val = float(high_ser.max())
                else:
                    highest_price_val = float("nan")

                # Low
                if "Low" in data.columns:
                    low_ser = _get_column_as_series(data, "Low")
                    lowest_price_val = float(low_ser.min())
                else:
                    lowest_price_val = float("nan")
                
                col1.metric("Latest Closing Price", f"{currency}{latest_close_val:.2f}")
                col2.metric("Highest Price", f"{currency}{highest_price_val:.2f}")
                col3.metric("Lowest Price", f"{currency}{lowest_price_val:.2f}")

                # Volume chart (if available) - avoid ambiguous boolean checks
                if "Volume" in data.columns:
                    vol_ser = _get_column_as_series(data, "Volume")
                    vol_sum = float(vol_ser.fillna(0).sum())
                    if vol_sum > 0:
                        st.subheader("📊 Trading Volume")
                        vol_plot = pd.DataFrame({"Volume": vol_ser.values}, index=data["Date"])
                        st.bar_chart(vol_plot["Volume"], use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")

