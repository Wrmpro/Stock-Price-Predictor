
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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
