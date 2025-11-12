# src/spp/feature_engineering.py
import pandas as pd
import numpy as np

def add_basic_features(df, close_col='Close'):
    df = df.copy()
    df['return'] = df[close_col].pct_change()
    # lag features
    for lag in [1,2,3,5,7,14]:
        df[f'lag_{lag}'] = df[close_col].shift(lag)
    # rolling statistics
    for window in [3,5,7,14,21]:
        df[f'roll_mean_{window}'] = df[close_col].rolling(window).mean()
        df[f'roll_std_{window}'] = df[close_col].rolling(window).std()
        df[f'roll_min_{window}'] = df[close_col].rolling(window).min()
        df[f'roll_max_{window}'] = df[close_col].rolling(window).max()
    # moving average crossovers
    df['ma_short'] = df[close_col].rolling(7).mean()
    df['ma_long'] = df[close_col].rolling(21).mean()
    df['ma_diff'] = df['ma_short'] - df['ma_long']
    # RSI (simple implementation)
    delta = df[close_col].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    roll_up = up.rolling(14).mean()
    roll_down = down.rolling(14).mean()
    rs = roll_up / (roll_down + 1e-8)
    df['rsi_14'] = 100 - (100 / (1 + rs))
    # MACD
    ema12 = df[close_col].ewm(span=12, adjust=False).mean()
    ema26 = df[close_col].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    # drop rows with NaNs
    df = df.dropna()
    return df
