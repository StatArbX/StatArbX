import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import unittest
from core.execution_engine import ExecutionEngine


class TestExecutionEngine(unittest.TestCase):

    def setUp(self):
        self.engine = ExecutionEngine()

    def test_initial_state(self):
        self.assertEqual(self.engine.position, 0)
        self.assertEqual(self.engine.compute_pnl(), 0.0)
        self.assertFalse(self.engine.is_in_position())
        self.assertEqual(self.engine.get_trade_log(), [])

    def test_enter_position(self):
        self.engine.enter(1, 100.0, 105.0)
        self.assertTrue(self.engine.is_in_position())
        self.assertEqual(self.engine.position, 1)
        self.assertEqual(self.engine.entry_price_a, 100.0)
        self.assertEqual(self.engine.entry_price_b, 105.0)

    def test_exit_long_position(self):
        self.engine.enter(1, 100.0, 105.0)
        self.engine.exit(102.0, 103.0)
        # PnL = (102 - 100) + (105 - 103) = 2 + 2 = 4
        self.assertFalse(self.engine.is_in_position())
        self.assertAlmostEqual(self.engine.compute_pnl(), 4.0)
        self.assertEqual(self.engine.get_trade_log(), [4.0])

    def test_exit_short_position(self):
        self.engine.enter(-1, 100.0, 105.0)
        self.engine.exit(98.0, 107.0)
        # PnL = (100 - 98) + (107 - 105) = 2 + 2 = 4
        self.assertFalse(self.engine.is_in_position())
        self.assertAlmostEqual(self.engine.compute_pnl(), 4.0)
        self.assertEqual(self.engine.get_trade_log(), [4.0])

    def test_exit_without_position_does_nothing(self):
        self.engine.exit(100.0, 100.0)  # Should not raise or update anything
        self.assertEqual(self.engine.position, 0)
        self.assertEqual(self.engine.compute_pnl(), 0.0)
        self.assertEqual(self.engine.get_trade_log(), [])


if __name__ == "__main__":
    unittest.main()
