import pandas as pd
from core.data_loader import DataLoader
from core.calc_spread import SignalGenerator


def test_spread_calculation():
    tickers = ["AAPL", "MSFT"]
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    # Load price data using DataLoader class
    loader = DataLoader()
    df = loader.download_data(tickers, start_date, end_date, use_cache=True)

    price_a = df["Adj Close"]["AAPL"]
    price_b = df["Adj Close"]["MSFT"]

    signal_gen = SignalGenerator(price_a=price_a, price_b=price_b)
    # Run spread calculation
    result = signal_gen.calculate_spread_and_thresholds()

    # Basic assertions to ensure spread stats are computed
    assert isinstance(result["beta"], float)
    assert isinstance(result["mean"], float)
    assert isinstance(result["std"], float)
    assert isinstance(result["zscore"], pd.Series)
    assert not result["zscore"].isna().all()

    # Optional: print one result for manual inspection
    print("Latest Z-score:", result["zscore"].iloc[-1])
