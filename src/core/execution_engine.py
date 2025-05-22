class ExecutionEngine:
    def __init__(self):
        self.position = 0  # 0 = no position, 1 = long, -1 = short
        self.entry_price_a = None
        self.entry_price_b = None
        self.trades = []
        self.pnl = 0.0

    def enter(self, direction: int, pa: float, pb: float):
        self.position = direction
        self.entry_price_a = pa
        self.entry_price_b = pb

    def exit(self, pa: float, pb: float):
        if self.position == 0:
            return

        if self.position == 1:
            trade_pnl = (pa - self.entry_price_a) + (self.entry_price_b - pb)
        else:
            trade_pnl = (self.entry_price_a - pa) + (pb - self.entry_price_b)

        self.trades.append(trade_pnl)
        self.pnl += trade_pnl
        self.position = 0

    def is_in_position(self) -> bool:
        return self.position != 0

    def get_trade_log(self):
        return self.trades

    def compute_pnl(self) -> float:
        return self.pnl
