class ExecutionEngine:
    def __init__(self):
        self.position = 0  # 0 = no position, 1 = long, -1 = short
        self.entry_price_a = None
        self.entry_price_b = None
        self.hedge_ratio = None
        self.trades = []
        self.pnl = 0.0

    def enter(self, direction: int, pa: float, pb: float, hedge_ratio: float):
        self.position = direction
        self.entry_price_a = pa
        self.entry_price_b = pb
        self.hedge_ratio = hedge_ratio

    def exit(self, pa: float, pb: float):
        if self.position == 0 or self.hedge_ratio is None:
            return

        ha = 1
        hb = self.hedge_ratio

        if self.position == 1:
            trade_pnl = ha * (pa - self.entry_price_a) + hb * (self.entry_price_b - pb)
        else:
            trade_pnl = ha * (self.entry_price_a - pa) + hb * (pb - self.entry_price_b)

        self.trades.append(trade_pnl)
        self.pnl += trade_pnl
        self.position = 0

    def is_in_position(self) -> bool:
        return self.position != 0

    def get_trade_log(self):
        return self.trades

    def compute_pnl(self) -> float:
        return self.pnl
