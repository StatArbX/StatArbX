import pandas as pd
from strategies.pairs_trading import PairsTrading


def test_pairs_trading_on_sample_data():
    # Load your test data (e.g., fixture, sample slice, or cached file)
    df = pd.read_csv(
        "data/test/tickers_2021_2024.csv", header=[0, 1], index_col=0, parse_dates=[0]
    )
    price_df = df["Adj Close"]

    # Instantiate and train strategy
    strategy = PairsTrading(price_df)

    print(f"Selected pairs: {strategy.pairs}")

    # Run strategy on test data
    trades = strategy.run(price_df)

    # Assertions
    assert isinstance(trades, list), "Trades should be a list"
    assert all(
        isinstance(t, (int, float)) for t in trades
    ), "All trades should be numeric PnLs"
    assert len(trades) > 0, "Expected at least one trade to be generated"
