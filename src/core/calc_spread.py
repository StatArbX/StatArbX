# --- Spread and Threshold Calculation ---
import pandas as pd
import statsmodels.api as sm
from typing import Dict, Any


def calculate_spread_and_thresholds(
    price_a: pd.Series, price_b: pd.Series
) -> Dict[str, Any]:
    """
    Calculate the spread and associated statistical thresholds between two price series.

    This function performs a linear regression of `price_a` on `price_b` to compute the spread,
    calculates its mean and standard deviation, and determines z-scores and thresholds for
    entry and exit signals in a trading strategy.

    Args:
        price_a (pd.Series): The first price series (dependent variable).
        price_b (pd.Series): The second price series (independent variable).

    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - "spread" (pd.Series): The calculated spread.
            - "zscore" (pd.Series): The z-scores of the spread.
            - "mean" (float): The mean of the spread.
            - "std" (float): The standard deviation of the spread.
            - "entry_threshold" (float): The z-score threshold for entering a trade.
            - "exit_threshold" (float): The z-score threshold for exiting a trade.
            - "beta" (float): The regression coefficient (beta) of `price_b`.
    """
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
