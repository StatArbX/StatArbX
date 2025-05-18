import os
import yfinance as yf
import pandas as pd
from typing import List

DATA_CACHE_PATH = "data/tickers"


def load_tickers(path: str = "data/tickers.txt") -> List[str]:
    """
    Load tickers from a text file.
    """
    with open(path, "r") as f:
        tickers = f.read().splitlines()
    return tickers


def download_data(
    tickers: List[str], start_date: str, end_date: str, use_cache: bool = True
) -> pd.DataFrame:
    start_year = pd.to_datetime(start_date).year
    end_year = pd.to_datetime(end_date).year
    filename = f"tickers_{start_year}_{end_year}.csv"
    data_path = os.path.join(DATA_CACHE_PATH, filename)

    if use_cache and os.path.exists(data_path):
        print(f"[CACHE HIT] Loading data from cache: {data_path}")
        data = pd.read_csv(data_path, header=[0, 1], index_col=0, parse_dates=[0])
        return data

    print(
        f"[CACHE MISS] Downloading data for {len(tickers)} tickers from Yahoo Finance..."
    )
    data = yf.download(
        tickers, start=start_date, end=end_date, auto_adjust=False, progress=False
    )

    if not isinstance(data.columns, pd.MultiIndex):
        data.columns = pd.MultiIndex.from_product(
            [tickers, data.columns], names=["Ticker", "PriceType"]
        )
    else:
        data.columns.names = ["Ticker", "PriceType"]

    data.dropna(how="all", inplace=True)
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    data.to_csv(data_path)
    print(f"[CACHE MISS] Data saved to cache: {data_path}")
    return data


if __name__ == "__main__":
    tickers = load_tickers()
    df = download_data(tickers, "2021-01-01", "2024-01-01", 3)
    print(df)
