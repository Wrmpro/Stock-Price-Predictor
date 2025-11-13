# src/main.py
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.spp.feature_engineering import add_basic_features
from src.spp.model import train_xgboost, xgb_predict, train_lstm, create_sequences, evaluate_regression
import joblib
import os

def load_data(symbol, start='2015-01-01', end=None):
    df = yf.download(symbol, start=start, end=end, progress=False)
    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[['Open','High','Low','Close','Volume']]
    return df

def prepare_tabular(df):
    df_feat = add_basic_features(df, close_col='Close')
    X = df_feat.drop(columns=['Open','High','Low','Close','Volume'], errors='ignore')
    y = df_feat['Close'].shift(-1).loc[X.index]   # predict next day's close
    # align
    mask = y.notna()
    X = X.loc[mask]
    y = y.loc[mask]
    return X, y

def train_pipeline_xgb(symbol='AAPL', save_path='models/xgb_model.json'):
    df = load_data(symbol)
    X, y = prepare_tabular(df)
    # time-based train-test split: last 20% as test
    split = int(len(X)*0.8)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    # scaler
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    # train
    bst = train_xgboost(X_train_s, y_train.values, X_val=X_test_s, y_val=y_test.values, num_boost_round=1000)
    # evaluate
    preds = xgb_predict(bst, X_test_s)
    metrics = evaluate_regression(y_test.values, preds)
    print("XGBoost metrics:", metrics)
    # save
    os.makedirs('models', exist_ok=True)
    bst.save_model(save_path)
    joblib.dump(scaler, 'models/xgb_scaler.pkl')
    return metrics

def train_pipeline_lstm(symbol='AAPL', seq_len=30, save_path='models/lstm.keras'):
    df = load_data(symbol)
    series = df['Close'].values.flatten()
    # scale series
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    series_s = scaler.fit_transform(series.reshape(-1,1)).flatten()
    model, hist = train_lstm(series_s, seq_len=seq_len, epochs=80)
    # save
    os.makedirs('models', exist_ok=True)
    model.save(save_path)
    joblib.dump(scaler, 'models/lstm_scaler.pkl')
    return model, hist

if __name__ == '__main__':
    # Train both models
    print("Training XGBoost on AAPL...")
    train_pipeline_xgb('AAPL')
    
    print("\nTraining LSTM on AAPL...")
    train_pipeline_lstm('AAPL')
    
    print("\n✅ All models trained successfully!")
    print("Models saved to:")
    print("  - models/xgb_model.json")
    print("  - models/xgb_scaler.pkl")
    print("  - models/lstm.keras")
    print("  - models/lstm_scaler.pkl")

