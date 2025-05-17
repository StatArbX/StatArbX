import pandas as pd
from statsmodels.tsa.stattools import coint
from typing import List, Tuple


def select_pairs(
    price_df: pd.DataFrame, corr_threshold: float = 0.85, max_pairs: int = 10
) -> List[Tuple[str, str, float]]:
    """
    Identify top cointegrated stock pairs with high correlation.

    Returns:
        List of tuples: (ticker1, ticker2, cointegration_pvalue)
    """
    tickers = price_df.columns
    returns = price_df.pct_change().dropna()
    corr_matrix = returns.corr()

    candidate_pairs = []

    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            t1, t2 = tickers[i], tickers[j]

            if corr_matrix.loc[t1, t2] >= corr_threshold:
                # Perform cointegration test
                score, pvalue, _ = coint(price_df[t1], price_df[t2])
                if not pd.isna(pvalue):
                    candidate_pairs.append((t1, t2, pvalue))

    # Sort by cointegration p-value (lower is better)
    candidate_pairs.sort(key=lambda x: x[2])

    return candidate_pairs[:max_pairs]
