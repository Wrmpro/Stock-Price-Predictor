
# src/spp/model.py
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import os

# XGBoost
import xgboost as xgb

# LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# Legacy functions for backward compatibility
def train_model(data):
    data = data[["Close"]].dropna()
    data["Target"] = data["Close"].shift(-1)
    data = data.dropna()

    X = data[["Close"]]
    y = data["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

def predict_prices(model, X_test):
    return model.predict(X_test)

# New XGBoost functions
def train_xgboost(X_train, y_train, X_val=None, y_val=None, params=None, num_boost_round=500):
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val) if X_val is not None else None
    if params is None:
        params = {
            'objective': 'reg:squarederror',
            'eval_metric': 'rmse',
            'eta': 0.05,
            'max_depth': 6,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'seed': 42
        }
    evals = [(dtrain, 'train')]
    if dval is not None: evals.append((dval, 'val'))
    bst = xgb.train(params, dtrain, num_boost_round=num_boost_round, evals=evals,
                    early_stopping_rounds=25 if dval is not None else None, verbose_eval=False)
    return bst

def xgb_predict(bst, X):
    d = xgb.DMatrix(X)
    return bst.predict(d)

# LSTM helpers
def create_sequences(values, seq_len=30):
    X, y = [], []
    for i in range(len(values) - seq_len):
        X.append(values[i:i+seq_len])
        y.append(values[i+seq_len])
    return np.array(X), np.array(y)

def build_lstm(input_shape, units=64, dropout=0.2):
    model = Sequential()
    model.add(LSTM(units, input_shape=input_shape, return_sequences=False))
    model.add(Dropout(dropout))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_lstm(series, seq_len=30, epochs=50, batch_size=32, val_split=0.1):
    # series: 1D numpy array of scaled values
    X, y = create_sequences(series, seq_len)
    X = X.reshape(X.shape[0], X.shape[1], 1)
    model = build_lstm((X.shape[1], 1))
    es = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)
    history = model.fit(X, y, epochs=epochs, batch_size=batch_size, validation_split=val_split, callbacks=[es], verbose=0)
    return model, history

# evaluation
def evaluate_regression(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)
    return {'rmse': float(rmse), 'mape': float(mape)}

# utilities to save/load models
def save_model(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(obj, path)

def load_xgb(path):
    bst = xgb.Booster()
    bst.load_model(path)
    return bst
