import numpy as np
import pandas as pd


def extract_features(prices_a: pd.Series, prices_b: pd.Series) -> np.ndarray:
    spread = prices_a - prices_b
    zscore = (spread - spread.mean()) / spread.std()
    corr = prices_a.corr(prices_b)
    spread_std = spread.std()
    vol_ratio = prices_a.pct_change().std() / prices_b.pct_change().std()

    return np.array([zscore.iloc[-1], spread_std, corr, vol_ratio])
