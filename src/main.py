from core.data_loader import load_tickers, download_data
from core.pair_selector import select_pairs
from core.backtest import backtest_pair

def main():
    tickers = load_tickers()
    df = download_data(tickers, "2021-01-01", "2024-01-01")

    # Work on adjusted close prices
    price_df = df["Adj Close"]
    selected_pairs = select_pairs(price_df)

    if not selected_pairs:
        print("[WARN] No pairs found. Try adjusting thresholds.")
        return

    for pair in selected_pairs:
        print(f"Backtesting pair: {pair[0]} and {pair[1]}")
        price_a = df["Adj Close"][pair[0]]
        price_b = df["Adj Close"][pair[1]]
        backtest_pair(price_a, price_b)

if __name__ == "__main__":
    main()
