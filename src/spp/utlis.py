
def evaluate_model(y_true, y_pred):
    from sklearn.metrics import mean_squared_error
    import numpy as np
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return {"MSE": mse, "RMSE": rmse}
