import pytest
import pandas as pd
from core.pair_selector import select_pairs
from core.data_loader import download_data


def test_select_pairs_returns_correct_type():
    # Use real tickers over a long enough range to ensure correlation and cointegration
    tickers = ["AAPL", "MSFT"]
    df = download_data(tickers, start_date="2022-01-01", end_date="2023-01-01")[
        "Adj Close"
    ]

    pairs = select_pairs(df, corr_threshold=0.7, max_pairs=5)

    assert isinstance(pairs, list)
    assert all(isinstance(p, tuple) and len(p) == 3 for p in pairs)
    assert all(
        isinstance(p[0], str) and isinstance(p[1], str) and isinstance(p[2], float)
        for p in pairs
    )
