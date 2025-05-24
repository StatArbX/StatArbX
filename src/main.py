from core.data_loader import DataLoader
from core.pair_selector import PairSelector
from core.calc_spread import SignalGenerator
from core.backtest import Backtester


def main():
    # === Load tickers and data ===
    loader = DataLoader()
    tickers = loader.load_tickers()
    df = loader.download_data(tickers, "2021-01-01", "2025-01-01")

    # === Split into train/test ===
    train_df = df.loc["2021-01-01":"2023-01-01"]
    test_df = df.loc["2023-01-02":"2025-01-01"]

    # === Work on adjusted close prices only ===
    train_price_df = train_df["Adj Close"]
    test_price_df = test_df["Adj Close"]

    # === Select pairs from training data ===
    selector = PairSelector(train_price_df)
    selected_pairs = selector.select_pairs()

    if not selected_pairs:
        print("[WARN] No pairs found. Try adjusting thresholds.")
        return

    # === Backtest on test data ===
    for pair in selected_pairs:
        print(f"Backtesting pair: {pair[0]} and {pair[1]}")
        price_a = test_price_df[pair[0]]
        price_b = test_price_df[pair[1]]

        signal_gen = SignalGenerator(price_a=price_a, price_b=price_b)
        backtester = Backtester(price_a, price_b, signal_gen)
        backtester.backtest_pair(entry_z=2.0, exit_z=0.0)


if __name__ == "__main__":
    main()
