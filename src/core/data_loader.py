import os
import yfinance as yf
import pandas as pd
from typing import List
from alpha_vantage.cryptocurrencies import CryptoCurrencies

DATA_CACHE_PATH = "data/tickers"
CRYPTO_TICKERS = "data/crypto.txt"


class DataLoader:
    def __init__(self, tickers_path: str = "data/tickers.txt"):
        self.tickers_path = tickers_path

        # ⚠️ HARD-CODED API KEY
        self.alpha = CryptoCurrencies(key="QHMLCHC13GJKULZC", output_format="pandas")

    def load_tickers(self) -> List[str]:
        with open(self.tickers_path, "r") as f:
            tickers = f.read().splitlines()
        return tickers

    def _download_crypto_data(self, ticker: str) -> pd.DataFrame:
        print(f"[ALPHA VANTAGE] Fetching crypto data for {ticker}...")
        df, _ = self.alpha.get_digital_currency_daily(symbol=ticker, market="USD")
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df[
            [
                "1a. open (USD)",
                "2a. high (USD)",
                "3a. low (USD)",
                "4a. close (USD)",
                "5. volume",
            ]
        ]
        df.columns = ["Open", "High", "Low", "Close", "Volume"]
        df["Adj Close"] = float("nan")
        df = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]]
        df.columns = pd.MultiIndex.from_product(
            [[ticker], df.columns], names=["Ticker", "PriceType"]
        )
        print(f"[ALPHA VANTAGE] Crypto data columns for {ticker}: {df.columns}")
        return df

    def _download_stock_data(
        self, tickers: List[str], start_date: str, end_date: str
    ) -> pd.DataFrame:
        print(f"[YFINANCE] Downloading stock data for {len(tickers)} ticker(s)...")
        data = yf.download(
            tickers, start=start_date, end=end_date, auto_adjust=False, progress=False
        )
        if not isinstance(data.columns, pd.MultiIndex):
            data.columns = pd.MultiIndex.from_product(
                [tickers, data.columns], names=["Ticker", "PriceType"]
            )
        else:
            data.columns.names = ["Ticker", "PriceType"]
        return data.dropna(how="all")

    def download_data(
        self, tickers: List[str], start_date: str, end_date: str, use_cache: bool = True
    ) -> pd.DataFrame:
        start_year = pd.to_datetime(start_date).year
        end_year = pd.to_datetime(end_date).year
        filename = f"tickers_{start_year}_{end_year}.csv"
        data_path = os.path.join(DATA_CACHE_PATH, filename)

        if use_cache and os.path.exists(data_path):
            print(f"[CACHE HIT] Loading data from cache: {data_path}")
            return pd.read_csv(data_path, header=[0, 1], index_col=0, parse_dates=True)

        # Load crypto tickers
        with open(CRYPTO_TICKERS, "r") as f:
            crypto_list = f.read().splitlines()

        stock_tickers = [t for t in tickers if t not in crypto_list]
        crypto_tickers = [t for t in tickers if t in crypto_list]

        print(f"[INFO] Crypto tickers to download: {crypto_tickers}")

        combined_data = []

        if stock_tickers:
            stock_data = self._download_stock_data(stock_tickers, start_date, end_date)
            # Select only the specified columns
            cols_to_keep = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
            stock_data = stock_data.loc[:, pd.IndexSlice[:, cols_to_keep]]
            combined_data.append(stock_data)

        for crypto in crypto_tickers:
            crypto_data = self._download_crypto_data(crypto)
            crypto_data = crypto_data.loc[start_date:end_date]
            combined_data.append(crypto_data)

        if not combined_data:
            print(
                "[WARNING] No data downloaded for given tickers. Returning empty DataFrame."
            )
            return pd.DataFrame()

        data = pd.concat(combined_data, axis=1).sort_index()
        print(f"[INFO] Combined data columns:\n{data.columns}")
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        data.to_csv(data_path)
        print(f"[CACHE MISS] Combined data saved to cache: {data_path}")
        return data
