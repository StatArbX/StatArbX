from core.data_loader import DataLoader
from utils.ml_utils import (
    generate_correlated_pairs,
    simulate_trade_pnl,
    evaluate_top_pairs,
)
from ml.model import PairProfitModel
from ml.features import extract_features
from ml.predict import predict_top_pairs
import pandas as pd
import numpy as np
import joblib


def main():
    loader = DataLoader()
    tickers = loader.load_tickers()
    df = loader.download_data(tickers, "2020-01-01", "2025-01-01")

    # Use Adj Close only
    adj_close = df["Adj Close"]  # shape: (dates, tickers)

    # ----------------------------
    # 1. TRAIN ML MODEL (2020–2021)
    # ----------------------------
    print("\n[ML TRAINING] Rolling over 2020–2021 to collect training data...")
    X, y = [], []

    window_size = 30
    trade_horizon = 30
    train_dates = pd.date_range("2020-01-15", "2021-12-15", freq="30D")

    for start_date in train_dates:
        end_date = start_date + pd.Timedelta(days=window_size)
        trade_end = end_date + pd.Timedelta(days=trade_horizon)

        price_window = adj_close.loc[start_date:end_date]
        trade_window = adj_close.loc[end_date:trade_end]

        pairs = generate_correlated_pairs(price_window)

        samples = []

        for a, b in pairs:
            try:
                fa = price_window[a].dropna()
                fb = price_window[b].dropna()
                features = extract_features(fa, fb)
                pnl = simulate_trade_pnl(trade_window[a], trade_window[b])
                if not np.isfinite(pnl):
                    continue
                samples.append((features, pnl))
            except Exception:
                continue

        if len(samples) < 10:
            continue  # not enough samples to rank

        samples.sort(key=lambda x: x[1])

        N = len(samples)
        cutoff = int(0.4 * N)

        for i, (features, pnl) in enumerate(samples):
            if i < cutoff:
                y.append(0)
                X.append(features)
            elif i >= N - cutoff:
                y.append(1)
                X.append(features)

    model = PairProfitModel()
    model.train(X, y)
    print(f"[ML] Trained on {len(X)} pairs")

    print("\n[ML PREDICTION] Scoring pairs for 2023...")
    test_price_df = adj_close.loc["2023-01-01":"2023-12-31"]
    score_window = adj_close.loc["2022-01-01":"2022-12-31"]  # Pre-trade features

    pairs = generate_correlated_pairs(score_window)
    top_pairs = predict_top_pairs(model, score_window, pairs, top_n=10)

    # ----------------------------
    # 3. BACKTEST USING SELECTED PAIRS
    # ----------------------------
    print("\n[BACKTEST] Starting backtest using top ML-selected pairs...")
    trades = evaluate_top_pairs(top_pairs, test_price_df)
    df = pd.DataFrame(trades)
    # ---- PnL Log ----
    print("\n[MODEL TRADE PnL LOG]")
    print(
        df[["a", "b", "score", "pnl"]]
        .sort_values("pnl", ascending=False)
        .to_string(index=False)
    )

    # ---- Summary Metrics ----
    total_pnl = df["pnl"].sum()
    avg_pnl = df["pnl"].mean()
    hit_rate = (df["pnl"] > 0).mean()
    sharpe = avg_pnl / df["pnl"].std() if df["pnl"].std() > 0 else 0

    print("\n[SUMMARY]")
    print(f"Total PnL      : {total_pnl:.2f}")
    print(f"Average PnL    : {avg_pnl:.2f}")
    print(f"Hit Rate       : {hit_rate:.2%}")
    print(f"Sharpe Ratio   : {sharpe:.2f}")

    print(f"\nBacktest completed with {len(trades)} trades executed.")
    joblib.dump(model, "models/pair_profit_model.pkl")


def test_model():
    """
    Test the model with a simple example.
    """
    model = joblib.load("models/pair_profit_model.pkl")

    # Load data
    loader = DataLoader()
    tickers = loader.load_tickers()
    df = loader.download_data(tickers, "2024-01-01", "2025-12-31")
    adj_close = df["Adj Close"]

    # Feature window: use 2024 to predict 2025
    score_window = adj_close.loc["2024-01-01":"2024-12-31"]
    test_price_df = adj_close.loc["2025-01-01":"2025-12-31"]

    # Generate pairs and predict
    pairs = generate_correlated_pairs(score_window)
    top_pairs = predict_top_pairs(model, score_window, pairs, top_n=10)

    # Evaluate trades
    trades = evaluate_top_pairs(top_pairs, test_price_df)
    df_trades = pd.DataFrame(trades)

    print("\n[Predicted Trades for 2025]")
    print(
        df_trades[["a", "b", "score", "pnl"]]
        .sort_values("pnl", ascending=False)
        .to_string(index=False)
    )

    # Metrics
    total_pnl = df_trades["pnl"].sum()
    hit_rate = (df_trades["pnl"] > 0).mean()
    sharpe = (
        df_trades["pnl"].mean() / df_trades["pnl"].std()
        if df_trades["pnl"].std() > 0
        else 0
    )

    print("\n[Summary]")
    print(f"Total PnL  : {total_pnl:.2f}")
    print(f"Hit Rate   : {hit_rate:.2%}")
    print(f"Sharpe     : {sharpe:.2f}")


if __name__ == "__main__":
    test_model()
