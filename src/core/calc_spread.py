# --- Spread and Threshold Calculation ---
import pandas as pd
import statsmodels.api as sm
from typing import Dict, Any


def calculate_spread_and_thresholds(
    price_a: pd.Series, price_b: pd.Series
) -> Dict[str, Any]:
    import pandas as pd

    # Combine series and drop NaNs
    X = sm.add_constant(price_b)
    df = pd.concat([price_a, X], axis=1).dropna()
    y = df.iloc[:, 0]
    X = df.iloc[:, 1:]

    # Run regression
    model = sm.OLS(y, X).fit()
    beta = model.params.iloc[0]  # since we dropped const, beta is now at index 0

    # Use aligned index to compute spread
    aligned_price_a = price_a.loc[df.index]
    aligned_price_b = price_b.loc[df.index]
    spread = aligned_price_a - beta * aligned_price_b

    # Stats
    mean = spread.mean()
    std = spread.std()
    zscore = (spread - mean) / std

    # Thresholds
    entry_threshold = 2.0
    exit_threshold = 0.0

    return {
        "spread": spread,
        "zscore": zscore,
        "mean": mean,
        "std": std,
        "entry_threshold": entry_threshold,
        "exit_threshold": exit_threshold,
        "beta": beta,
    }
