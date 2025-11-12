# app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from datetime import datetime, timedelta
from src.spp.feature_engineering import add_basic_features
from src.spp.model import xgb_predict, create_sequences
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Stock Price Predictor", page_icon="📈", layout="wide")
st.title("📈 Stock Price Predictor & Visualizer")

# Initialize session state
if 'symbol' not in st.session_state:
    st.session_state.symbol = "AAPL"

# Sidebar
st.sidebar.header("Configuration")

# Use session state directly for the text input
symbol_input = st.sidebar.text_input("Ticker (e.g., AAPL or RELIANCE.NS)", value=st.session_state.symbol)
# Update session state when sidebar input changes
if symbol_input:
    st.session_state.symbol = symbol_input
start = st.sidebar.date_input("Start date", value=datetime(2018,1,1))
end = st.sidebar.date_input("End date", value=datetime.today())

st.sidebar.markdown(
    """
    ✅ **Examples**  
    - US Stocks: `AAPL`, `TSLA`, `MSFT`  
    - Indian Stocks: `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`  
    - Indices: `^NSEI` (NIFTY 50), `^BSESN` (SENSEX)
    """
)

# Quick access buttons
st.markdown("### ✅ Quick Stock Selection")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("AAPL"):
        st.session_state.symbol = "AAPL"
        st.rerun()
with col2:
    if st.button("TSLA"):
        st.session_state.symbol = "TSLA"
        st.rerun()
with col3:
    if st.button("MSFT"):
        st.session_state.symbol = "MSFT"
        st.rerun()
with col4:
    if st.button("RELIANCE.NS"):
        st.session_state.symbol = "RELIANCE.NS"
        st.rerun()

# Data loading
if st.button("Load Data"):
    df = yf.download(st.session_state.symbol, start=start, end=end, progress=False)
    if df.empty:
        st.error("No data found for symbol.")
    else:
        st.success(f"Loaded {len(df)} rows for {st.session_state.symbol}.")
        st.dataframe(df.tail(), use_container_width=True)
        
        # Basic visualization
        st.subheader("📊 Closing Price Over Time")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price'))
        fig.update_layout(xaxis_title="Date", yaxis_title="Price", height=400)
        st.plotly_chart(fig, use_container_width=True)

# Model prediction section
st.markdown("---")
st.subheader("🤖 ML Prediction")

model_choice = st.selectbox("Select Model", ["XGBoost (tabular)", "LSTM (sequence)"])

if st.button("Predict Next Days"):
    df = yf.download(st.session_state.symbol, start=start, end=end, progress=False)
    if df.empty:
        st.error("No data found.")
    else:
        if model_choice.startswith("XGBoost"):
            # load model and scaler
            if not os.path.exists('models/xgb_model.json') or not os.path.exists('models/xgb_scaler.pkl'):
                st.error("❌ XGBoost model not found. Train it using: `python src/main.py`")
                st.info("💡 Run the following command in your terminal:\n```bash\npython src/main.py\n```")
            else:
                with st.spinner("Loading model and generating predictions..."):
                    scaler = joblib.load('models/xgb_scaler.pkl')
                    bst = xgb.Booster()
                    bst.load_model('models/xgb_model.json')
                    df_feat = add_basic_features(df, close_col='Close')
                    X = df_feat.drop(columns=['Open','High','Low','Close','Volume'], errors='ignore')
                    X_s = scaler.transform(X)
                    preds = xgb_predict(bst, X_s)
                    
                    # show last actual vs predicted
                    last_n = min(200, len(df_feat))
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df_feat.index[-last_n:], 
                                            y=df['Close'].loc[df_feat.index][-last_n:], 
                                            name='Actual', mode='lines'))
                    fig.add_trace(go.Scatter(x=df_feat.index[-last_n:], 
                                            y=preds[-last_n:], 
                                            name='Predicted', mode='lines'))
                    fig.update_layout(title=f"{st.session_state.symbol} - Actual vs Predicted Prices",
                                     xaxis_title="Date", 
                                     yaxis_title="Price",
                                     height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show recent predictions
                    st.write("📋 Recent Predictions:")
                    pred_df = pd.DataFrame({
                        'Date': df_feat.index[-10:],
                        'Actual': df['Close'].loc[df_feat.index][-10:].values,
                        'Predicted': preds[-10:]
                    })
                    pred_df['Error'] = abs(pred_df['Actual'] - pred_df['Predicted'])
                    pred_df['Error %'] = (pred_df['Error'] / pred_df['Actual'] * 100).round(2)
                    st.dataframe(pred_df, use_container_width=True)
        else:
            # LSTM model
            # Check for both .keras and .h5 formats (backward compatibility)
            lstm_model_path = None
            if os.path.exists('models/lstm.keras'):
                lstm_model_path = 'models/lstm.keras'
            elif os.path.exists('models/lstm.h5'):
                lstm_model_path = 'models/lstm.h5'
            
            if not lstm_model_path or not os.path.exists('models/lstm_scaler.pkl'):
                st.error("❌ LSTM model not found. Train it using: `python src/main.py`")
                st.info("💡 Run the following command in your terminal:\n```bash\npython src/main.py\n```\nThis will create both XGBoost and LSTM models.")
            else:
                with st.spinner("Loading LSTM model and generating predictions..."):
                    from tensorflow import keras
                    from sklearn.preprocessing import MinMaxScaler
                    
                    # Load model and scaler
                    model = keras.models.load_model(lstm_model_path)
                    scaler_lstm = joblib.load('models/lstm_scaler.pkl')
                    
                    # Prepare sequences
                    series = df['Close'].values
                    series_s = scaler_lstm.transform(series.reshape(-1,1)).flatten()
                    seq_len = 30
                    X_seq, _ = create_sequences(series_s, seq_len=seq_len)
                    X_seq = X_seq.reshape(X_seq.shape[0], X_seq.shape[1], 1)
                    
                    # Predict
                    preds_s = model.predict(X_seq, verbose=0).flatten()
                    preds = scaler_lstm.inverse_transform(preds_s.reshape(-1,1)).flatten()
                    
                    # Align predictions with dates (predictions start at index seq_len)
                    pred_dates = df.index[seq_len:seq_len+len(preds)]
                    
                    # Show predictions
                    last_n = min(200, len(preds))
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=pred_dates[-last_n:], 
                                            y=df['Close'].loc[pred_dates][-last_n:], 
                                            name='Actual', mode='lines'))
                    fig.add_trace(go.Scatter(x=pred_dates[-last_n:], 
                                            y=preds[-last_n:], 
                                            name='Predicted', mode='lines'))
                    fig.update_layout(title=f"{st.session_state.symbol} - LSTM Actual vs Predicted Prices",
                                     xaxis_title="Date", 
                                     yaxis_title="Price",
                                     height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show recent predictions
                    st.write("📋 Recent Predictions:")
                    pred_df = pd.DataFrame({
                        'Date': pred_dates[-10:],
                        'Actual': df['Close'].loc[pred_dates][-10:].values,
                        'Predicted': preds[-10:]
                    })
                    pred_df['Error'] = abs(pred_df['Actual'] - pred_df['Predicted'])
                    pred_df['Error %'] = (pred_df['Error'] / pred_df['Actual'] * 100).round(2)
                    st.dataframe(pred_df, use_container_width=True)

st.markdown("---")
st.markdown("""
### 💡 Tips
- **XGBoost**: Fast, strong baseline for tabular time-series features. Train first for best results.
- **LSTM**: Requires more data (3+ years) and GPU if available for longer-horizon forecasting.
- **Training**: Run `python src/main.py` to train models before prediction.
""")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, XGBoost, and TensorFlow")

