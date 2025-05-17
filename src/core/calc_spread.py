# --- Spread and Threshold Calculation ---
import pandas as pd
import statsmodels.api as sm
from typing import Dict, Any

def calculate_spread_and_thresholds(price_a: pd.Series, price_b: pd.Series) -> Dict[str, Any]:
    """
    Calculate the spread between two price series using linear regression to determine the hedge ratio (beta),
    and compute mean, standard deviation, and z-score thresholds for trading.

    Args:
        price_a (pd.Series): Price series of stock A.
        price_b (pd.Series): Price series of stock B.

    Returns:
        dict: Dictionary containing spread, mean, std, zscore series, and thresholds.
    """
    # Step 1: Regress A on B to get hedge ratio (beta)
    X = sm.add_constant(price_b)
    model = sm.OLS(price_a, X).fit()
    beta = model.params.iloc[1]

    # Step 2: Calculate spread using hedge ratio
    spread = price_a - beta * price_b

    # Step 3: Compute mean and standard deviation of spread
    mean = spread.mean()
    std = spread.std()

    # Step 4: Compute z-score to normalize spread
    zscore = (spread - mean) / std  # type: ignore

    # Step 5: Define default thresholds for trading signals
    entry_threshold = 2.0
    exit_threshold = 0.0

    return {
        "spread": spread,
        "zscore": zscore,
        "mean": mean,
        "std": std,
        "entry_threshold": entry_threshold,
        "exit_threshold": exit_threshold,
        "beta": beta
    }
