import pandas as pd
from core.execution_engine import ExecutionEngine
from strategies.base import Strategy


class Backtester:
    def __init__(self, backtest_data: pd.DataFrame, strategy: Strategy):
        self.backtest_data = backtest_data
        self.strategy = strategy
        self.execution = ExecutionEngine()

    def backtest(self):
        """
        Run the backtest using the provided strategy and backtest data.
        :return: List of trades executed during the backtest.
        """
        trades = []
        trades = self.strategy.run(self.backtest_data)

        return trades
