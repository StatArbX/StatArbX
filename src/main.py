from core.data_loader import DataLoader
from core.backtest import Backtester
from strategies.pairs_trading import PairsTrading
from ml.model import PairProfitModel
from ml.features import extract_features
from ml.predict import predict_top_pairs
#from core.pair_selector import generate_all_pairs
#from utils.simulate import simulate_trade_pnl  # You or your partner's trade logic

import pandas as pd
import numpy as np

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

    window_size = 15
    trade_horizon = 15
    train_dates = pd.date_range("2020-01-15", "2021-12-15", freq="15D")

    for start_date in train_dates:
        end_date = start_date + pd.Timedelta(days=window_size)
        trade_end = end_date + pd.Timedelta(days=trade_horizon)
        
        price_window = adj_close.loc[start_date:end_date]
        trade_window = adj_close.loc[end_date:trade_end]

        if len(price_window) < window_size or len(trade_window) < trade_horizon:
            continue

        pairs = generate_all_pairs(price_window.columns)

        for a, b in pairs:
            try:
                fa = price_window[a].dropna()
                fb = price_window[b].dropna()
                features = extract_features(fa, fb)
                pnl = simulate_trade_pnl(fa, fb, trade_window[a], trade_window[b])
                label = 1 if pnl > 0 else 0

                X.append(features)
                y.append(label)
            except:
                continue

    model = PairProfitModel()
    model.train(X, y)
    print(f"[ML] Trained on {len(X)} pairs")

    # ----------------------------
    # 2. PREDICT TOP PAIRS (2023)
    # ----------------------------
    print("\n[ML PREDICTION] Scoring pairs for 2023...")
    test_price_df = adj_close.loc["2023-01-01":"2024-12-31"]
    score_window = adj_close.loc["2022-12-01":"2022-12-31"]  # Pre-trade features

    pairs = generate_all_pairs(score_window.columns)
    top_pairs = predict_top_pairs(model, score_window, pairs, top_n=10)

    # ----------------------------
    # 3. BACKTEST USING SELECTED PAIRS
    # ----------------------------
    print(f"\n[BACKTEST] Starting backtest using top ML-selected pairs...")
    strategy = PairsTrading(test_price_df, selected_pairs=top_pairs) 
    backtester = Backtester(test_price_df, strategy)
    trades = backtester.backtest()
    print(f"\nBacktest completed with {len(trades)} trades executed.")


if __name__ == "__main__":
    main()