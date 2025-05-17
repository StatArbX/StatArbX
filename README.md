# StatArbX

**StatArbX** is a quantitative trading engine designed to identify statistically correlated stock pairs and exploit temporary pricing inefficiencies through a mean-reverting strategy. Built as a first iteration MVP, this project focuses on the implementation of a pair trading strategy using historical data, statistical tests, and simple backtesting logic.

## 📊 Objective

To develop a minimum viable product (MVP) that:
- Detects related stock pairs using statistical methods
- Computes spread and trading thresholds
- Backtests pair trading signals on historical data
- Lays the foundation for a live trading system

## 🚀 Current MVP Workflow

1. **Data Loading**
   - Pull historical price data using `yfinance` or another API
   - Preprocess and normalize time series

2. **Pair Selection**
   - Identify candidate stock pairs based on correlation and cointegration
   - Filter for statistically significant relationships

3. **Spread Computation**
   - Use linear regression to compute spread between each pair
   - Calculate Z-score for identifying trading opportunities
   - Define entry and exit thresholds

4. **Backtesting Engine**
   - Simulate trades based on Z-score triggers
   - Track PnL, Sharpe ratio, drawdowns, and win rate
   - Visualize price charts, spreads, and trade points

## 🛠️ Tech Stack

- Python
- Pandas, NumPy, statsmodels
- yFinance for data ingestion
- Matplotlib for visualizations

## 📈 Future Plans

- Improve pair selection with dynamic filtering
- Add transaction cost modeling
- Integrate with live market data feeds
- Build a real-time execution engine with order book integration

---

📬 Feel free to fork, contribute, or raise issues!
