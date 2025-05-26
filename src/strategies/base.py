from abc import ABC, abstractmethod


class Strategy(ABC):
    """
    Abstract base class for strategies.
    All strategies should inherit from this class and implement the `execute` method.
    """

    @abstractmethod
    def run(self, test_data: dict):
        """
        Execute the strategy with the given arguments.
        :param market_data: Dictionary containing market data required for the strategy.
        :return: Result of the strategy execution.
        """
        pass
