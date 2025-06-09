import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def extract_features(prices_a: pd.Series, prices_b: pd.Series) -> np.ndarray:
    prices_a = prices_a.dropna()
    prices_b = prices_b.dropna()

    spread = prices_a - prices_b
    spread_std = spread.std()
    if spread_std == 0 or np.isnan(spread_std):
        spread_std = 1e-5  # prevent divide by zero by using a small number

    zscore = (spread - spread.mean()) / spread_std
    z = zscore.iloc[-1] if not zscore.empty else 0.0

    corr = prices_a.corr(prices_b)
    if np.isnan(corr):
        corr = 0.0

    vola = prices_a.pct_change().std()
    volb = prices_b.pct_change().std()
    vol_ratio = vola / volb if volb != 0 else 1.0

    # Half-life estimation
    lagged = spread.shift(1).dropna()
    delta = spread.diff().dropna()
    if len(lagged) == len(delta):
        reg = LinearRegression().fit(lagged.values.reshape(-1, 1), delta.values)
        halflife = -np.log(2) / reg.coef_[0]
    else:
        halflife = 10

    return np.array([z, spread_std, corr, vol_ratio, halflife])
