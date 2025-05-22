import pandas as pd
from core.execution_engine import ExecutionEngine
from core.calc_spread import SignalGenerator


class Backtester:
    def __init__(
        self, price_a: pd.Series, price_b: pd.Series, signal_gen: SignalGenerator
    ):
        self.price_a = price_a
        self.price_b = price_b
        self.signal_gen = signal_gen
        self.execution = ExecutionEngine()

    def backtest_pair(self, entry_z: float = 2.0, exit_z: float = 0.0):
        result = self.signal_gen.calculate_spread_and_thresholds()
        zscore = result["zscore"]

        for date in zscore.index:
            z = zscore.loc[date]
            pa = self.price_a.loc[date]
            pb = self.price_b.loc[date]

            if not self.execution.is_in_position():
                if z > entry_z:
                    self.execution.enter(-1, pa, pb)  # SHORT A, LONG B
                elif z < -entry_z:
                    self.execution.enter(1, pa, pb)  # LONG A, SHORT B
            else:
                if (self.execution.position == -1 and z < exit_z) or \
                   (self.execution.position == 1 and z > exit_z):
                    self.execution.exit(pa, pb)

        trades = self.execution.get_trade_log()
        pnl = self.execution.compute_pnl()

        print(f"Total Trades: {len(trades)}")
        print(f"Total PnL: {pnl:.2f}")
        if trades:
            print(f"Avg PnL per Trade: {pnl / len(trades):.2f}")
            print(f"Win Rate: {sum(1 for t in trades if t > 0) / len(trades) * 100:.2f}%")

        return trades
