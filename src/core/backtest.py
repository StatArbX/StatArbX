import pandas as pd
from core.data_loader import load_tickers
from core.data_loader import download_data
from core.calc_spread import calculate_spread_and_thresholds
from core.pair_selector import select_pairs

def backtest_pair(price_a: pd.Series, price_b: pd.Series, entry_z: float = 2.0, exit_z: float = 0.0):
    result = calculate_spread_and_thresholds(price_a, price_b)
    zscore = result["zscore"]
    spread = result["spread"]

    position = 0  # 0 = no position, 1 = long spread, -1 = short spread
    entry_price_a = entry_price_b = 0.0
    trades = []
    pnl = 0.0

    for date in zscore.index:
        z = zscore.loc[date]
        pa = price_a.loc[date]
        pb = price_b.loc[date]

        if position == 0:
            if z > entry_z:
                # SHORT A, LONG B
                position = -1
                entry_price_a, entry_price_b = pa, pb
            elif z < -entry_z:
                # LONG A, SHORT B
                position = 1
                entry_price_a, entry_price_b = pa, pb

        elif position == -1 and z < exit_z:
            # Exit SHORT A, LONG B
            trade_pnl = (entry_price_a - pa) + (pb - entry_price_b)
            trades.append(trade_pnl)
            pnl += trade_pnl
            position = 0

        elif position == 1 and z > exit_z:
            # Exit LONG A, SHORT B
            trade_pnl = (pa - entry_price_a) + (entry_price_b - pb)
            trades.append(trade_pnl)
            pnl += trade_pnl
            position = 0

    print(f"Total Trades: {len(trades)}")
    print(f"Total PnL: {pnl:.2f}")
    if trades:
        print(f"Avg PnL per Trade: {pnl / len(trades):.2f}")
        print(f"Win Rate: {sum(1 for t in trades if t > 0) / len(trades) * 100:.2f}%")

if __name__ == "__main__":
    tickers = load_tickers()
    df = download_data(tickers, "2022-01-01", "2023-01-01")

    selected_pairs = select_pairs(df["Adj Close"])

    for pair in selected_pairs:
        print(f"Backtesting pair: {pair[0]} and {pair[1]}")
        price_a = df["Adj Close"][pair[0]]
        price_b = df["Adj Close"][pair[1]]
        backtest_pair(price_a, price_b)