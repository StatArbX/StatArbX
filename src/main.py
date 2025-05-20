from core.data_loader import DataLoader
from core.pair_selector import PairSelector
from core.calc_spread import SignalGenerator
from core.backtest import Backtester


def main():
    # === Load tickers and data ===
    loader = DataLoader()
    tickers = loader.load_tickers()
    df = loader.download_data(tickers, "2021-01-01", "2024-01-01")

    # === Work on adjusted close prices only ===
    price_df = df["Adj Close"]

    # === Select pairs ===
    selector = PairSelector(price_df)
    selected_pairs = selector.select_pairs()

    if not selected_pairs:
        print("[WARN] No pairs found. Try adjusting thresholds.")
        return

    for pair in selected_pairs:
        print(f"Backtesting pair: {pair[0]} and {pair[1]}")
        price_a = price_df[pair[0]]
        price_b = price_df[pair[1]]

        signal_gen = SignalGenerator(price_a=price_a, price_b=price_b)
        backtester = Backtester(price_a, price_b, signal_gen)
        backtester.backtest_pair(entry_z=2.0, exit_z=0.0)


if __name__ == "__main__":
    main()
