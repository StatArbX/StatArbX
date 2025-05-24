import pandas as pd
from core.calc_spread import SignalGenerator


def test_spread_calculation():

    df = pd.read_csv(
        "data/test/tickers_2021_2024.csv", header=[0, 1], index_col=2, parse_dates=[0]
    )

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
