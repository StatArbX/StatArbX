from strategies.base import Strategy
from core.pair_selector import PairSelector
from core.calc_spread import SignalGenerator
from core.execution_engine import ExecutionEngine
import pandas as pd


class PairsTrading(Strategy):
    """
    Pairs Trading Strategy.
    This strategy identifies pairs of assets that historically move together and trades on the divergence from their historical relationship.
    """

    def __init__(self, train_data: pd.DataFrame):
        """
        Initialize the Pairs Trading strategy with a pair selector and signal generator.
        :param signal_generator: Instance of SignalGenerator to generate trading signals based on the selected pairs.
        """
        self.pair_selector = PairSelector(train_data)
        self.pairs = self.pair_selector.select_pairs()
        self.entry_z = 2.0
        self.exit_z = 0.0
        self.train_data = train_data
        self.execution_engine = None

    def run(self, test_data: pd.DataFrame):
        """
        Run the pairs trading strategy on the test data.
        :param test_data: DataFrame containing the test market data.
        :return: List of trades executed during the backtest.
        """
        trades = []
        for (
            ticker_a,
            ticker_b,
            _,
        ) in self.pairs:  # Need to check whether training ticker is in test data
            price_a = test_data[ticker_a]
            price_b = test_data[ticker_b]
            self.execution_engine = ExecutionEngine()
            signal_generator = SignalGenerator(price_a, price_b)
            signal_data = signal_generator.calculate_spread_and_thresholds()
            zscore = signal_data["zscore"]

            for date in test_data.index:
                pa = price_a.loc[date]
                pb = price_b.loc[date]

                if date not in zscore:
                    continue

                z = zscore.loc[date]

                if not self.execution_engine.is_in_position():
                    if z > self.entry_z:
                        self.execution_engine.enter(-1, pa, pb)
                    elif z < -self.entry_z:
                        self.execution_engine.enter(1, pa, pb)
                else:
                    if (self.execution_engine.position == -1 and z < self.exit_z) or (
                        self.execution_engine.position == 1 and z > self.exit_z
                    ):
                        self.execution_engine.exit(pa, pb)

            trades.extend(self.execution_engine.get_trade_log())
            pnl = self.execution_engine.compute_pnl()

            print(f"Ticker Pair: {ticker_a} - {ticker_b}")
            print(f"Total Trades: {len(trades)}")
            print(f"Total PnL: {pnl:.2f}")
            if trades:
                print(f"Avg PnL per Trade: {pnl / len(trades):.2f}")
                print(
                    f"Win Rate: {sum(1 for t in trades if t > 0) / len(trades) * 100:.2f}%"
                )

        return trades
