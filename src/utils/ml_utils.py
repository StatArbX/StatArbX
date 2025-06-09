from typing import List, Tuple
import pandas as pd
from core.calc_spread import SignalGenerator
from core.execution_engine import ExecutionEngine


def generate_correlated_pairs(
    price_df: pd.Series, corr_threshold=0.6
) -> List[Tuple[str, str]]:
    returns = price_df.pct_change().dropna()
    corr = returns.corr()

    pairs = [
        (a, b)
        for i, a in enumerate(corr.columns)
        for j, b in enumerate(corr.columns)
        if i < j and corr.loc[a, b] > corr_threshold
    ]
    return pairs


def simulate_trade_pnl(price_a: pd.Series, price_b: pd.Series) -> float:
    """
    Simulate the PnL of a trade between two assets using z-score-based entry/exit.

    Args:
        price_a (pd.Series): Prices of asset A (indexed by date).
        price_b (pd.Series): Prices of asset B (indexed by date).

    Returns:
        float: Total PnL from simulated trade.
    """
    signal_generator = SignalGenerator(price_a, price_b)
    signal_data = signal_generator.calculate_spread_and_thresholds()
    zscore = signal_data["zscore"]
    beta = signal_data["beta"]

    engine = ExecutionEngine()
    for date in price_a.index:
        if date not in zscore:
            continue

        pa = price_a.loc[date]
        pb = price_b.loc[date]
        z = zscore.loc[date]

        if not engine.is_in_position():
            if z > 2:
                engine.enter(-1, pa, pb, beta)  # short spread: short A, long βB
            elif z < -2:
                engine.enter(1, pa, pb, beta)  # long spread: long A, short βB
        else:
            if (engine.position == -1 and z < 0) or (engine.position == 1 and z > 0):
                engine.exit(pa, pb)

    # Force exit at last timestamp if still holding
    if engine.is_in_position():
        engine.exit(price_a.iloc[-1], price_b.iloc[-1])

    return engine.compute_pnl()


def evaluate_top_pairs(top_pairs, test_price_df):
    results = []
    for ticker_a, ticker_b, score in top_pairs:
        price_a = test_price_df[ticker_a]
        price_b = test_price_df[ticker_b]

        pnl = simulate_trade_pnl(price_a, price_b)
        results.append({"a": ticker_a, "b": ticker_b, "score": score, "pnl": pnl})
    return results
