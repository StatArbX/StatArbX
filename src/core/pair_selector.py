import os
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
from typing import List, Tuple

CACHE_DIR = "data"
CACHE_FILE = os.path.join(CACHE_DIR, "cointegration_cache.csv")


def select_pairs(
    price_df: pd.DataFrame,
    corr_threshold: float = 0.6,
    max_pairs: int = 10,
    pval_cutoff: float = 0.05,
    use_cache: bool = True
) -> List[Tuple[str, str, float]]:
    tickers = list(price_df.columns)
    returns = price_df.pct_change().dropna()
    corr_matrix = returns.corr()

    candidate_pairs = []

    # Load cached p-values if available
    cache_df = None
    if use_cache and os.path.exists(CACHE_FILE):
        print(f"[CACHE HIT] Loading cointegration scores from {CACHE_FILE}")
        cache_df = pd.read_csv(CACHE_FILE)
    else:
        print(f"[CACHE MISS] Recomputing cointegration scores")

    # To write new cache
    new_cache = []

    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            t1, t2 = tickers[i], tickers[j]

            # Correlation filter
            if corr_matrix.loc[t1, t2] < corr_threshold:
                continue

            # Try cache first
            pval = None
            if cache_df is not None:
                row = cache_df[(cache_df["A"] == t1) & (cache_df["B"] == t2)]
                if not row.empty:
                    pval = float(row["pvalue"].values[0])

            if pval is None:
                # Compute log-price cointegration
                p1 = np.log(price_df[t1].dropna())
                p2 = np.log(price_df[t2].dropna())
                df_pair = pd.concat([p1, p2], axis=1).dropna()
                if len(df_pair) < 100:
                    continue
                _, pval, _ = coint(df_pair.iloc[:, 0], df_pair.iloc[:, 1])
                new_cache.append({"A": t1, "B": t2, "pvalue": pval})

            if not pd.isna(pval) and pval < pval_cutoff:
                candidate_pairs.append((t1, t2, pval))

    # Save new cache if needed
    if new_cache and use_cache:
        new_cache_df = pd.DataFrame(new_cache)
        new_cache_df.to_csv(CACHE_FILE, index=False)
        print(f"[CACHE SAVE] Cached {len(new_cache)} new scores to {CACHE_FILE}")

    # Sort and return top N
    candidate_pairs.sort(key=lambda x: x[2])
    return candidate_pairs[:max_pairs]
