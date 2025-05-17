import yfinance as yf
import pandas as pd
from typing import List


def load_tickers(path: str = "data/tickers.txt") -> List[str]:
    """
    Load tickers from a text file.
    """
    with open(path, "r") as f:
        tickers = f.read().splitlines()
    return tickers


def download_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Download historical stock data from Yahoo Finance.
    """
    data = yf.download(
        tickers, start=start_date, end=end_date, auto_adjust=False, progress=False
    )

    return data.dropna(how="all")
