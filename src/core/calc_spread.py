import pandas as pd
import statsmodels.api as sm
from typing import Dict, Any


def calculate_spread_and_thresholds(
    price_a: pd.Series, price_b: pd.Series
) -> Dict[str, Any]:
    """
    Calculate spread and z-score for pairs trading using linear regression.

    Args:
        price_a (pd.Series): Dependent variable (e.g., GOOGL)
        price_b (pd.Series): Independent variable (e.g., MSFT)

    Returns:
        Dict[str, Any]: Keys: spread, zscore, mean, std, beta, intercept, etc.
    """
    # Align series and drop NaNs
    df = pd.concat([price_a, price_b], axis=1).dropna()
    y = df.iloc[:, 0]
    x = sm.add_constant(df.iloc[:, 1])

    # Linear regression
    model = sm.OLS(y, x).fit()
    intercept = model.params["const"]
    beta = model.params[price_b.name]  # This is the slope

    # Compute spread using the full regression equation
    spread = y - (intercept + beta * df.iloc[:, 1])

    # Z-score of spread
    mean = spread.mean()
    std = spread.std()
    zscore = (spread - mean) / std

    return {
        "spread": spread,
        "zscore": zscore,
        "mean": mean,
        "std": std,
        "entry_threshold": 2.0,
        "exit_threshold": 0.0,
        "beta": beta,
        "intercept": intercept,
    }
