from core.data_loader import DataLoader
from core.backtest import Backtester
from strategies.pairs_trading import PairsTrading


def main():
    # === Load tickers and data ===
    loader = DataLoader()
    tickers = loader.load_tickers()
    df = loader.download_data(tickers, "2021-01-01", "2025-01-01")

    # Work only with Adjusted Close prices
    adj_close = df["Adj Close"]  # shape: (dates, tickers)

    # Split into training and testing sets
    train_price_df = adj_close.loc["2021-01-01":"2022-12-31"]
    test_price_df = adj_close.loc["2023-01-01":"2024-12-31"]

    strategy = PairsTrading(train_price_df)

    backtester = Backtester(test_price_df, strategy)
    trades = backtester.backtest()
    print(f"Backtest completed with {len(trades)} trades executed.")


if __name__ == "__main__":
    main()
