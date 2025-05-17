# StatArbX

**StatArbX** is a quantitative trading engine designed to identify statistically correlated stock pairs and exploit temporary pricing inefficiencies through a mean-reverting strategy. Built as a first iteration MVP, this project focuses on the implementation of a pair trading strategy using historical data, statistical tests, and simple backtesting logic.

---

## 📊 Objective

To develop a minimum viable product (MVP) that:
- Detects related stock pairs using statistical methods
- Computes spread and trading thresholds
- Backtests pair trading signals on historical data
- Lays the foundation for a live trading system

---

## 🚀 Current MVP Workflow

1. **Data Loading**
   - Pull historical price data using `yfinance`
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

---

## 🛠️ Tech Stack

- Python
- Pandas, NumPy, statsmodels
- yFinance for data ingestion
- Matplotlib for visualizations

---

## 🧪 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/StatArbX/StatArbX.git
cd StatArbX
````

### 2. Create a Virtual Environment and Install Dependencies

```bash
make setup
```

This will:

* Create a `.venv/` folder
* Install all dependencies from `requirements.txt`

---

## ▶️ Running the Project

```bash
make run
```

> Runs the strategy (once `src/main.py` is implemented).

---

## 🧪 Running Tests

```bash
make test
```

This will:

* Format code with `black`
* Lint using `ruff`
* Run all `pytest` tests in the `tests/` folder

---

## 📦 Freezing Dependencies

```bash
make freeze
```

Exports the current virtual environment to `requirements.txt`.

---

## 🧹 Cleaning Up

```bash
make clean
```

Removes:

* `.venv/`
* `__pycache__/`
* Python bytecode and log files

---

## 📁 Project Directory Structure

```
StatArbX/
├── data/             # Market data & ticker list
├── notebooks/        # EDA, visualization, experiments
├── src/              # Core strategy logic
├── tests/            # Unit + integration tests
├── .gitignore
├── Makefile
├── README.md
├── requirements.txt
└── .env              # (not tracked — for secrets or config)
```

---

## 📈 Future Plans

* Improve pair selection with dynamic filtering
* Add transaction cost modeling
* Integrate with live market data feeds
* Build a real-time execution engine with order book integration

---

📬 Feel free to fork, contribute, or raise issues!

```

---

Let me know if you'd like this split into sections in `docs/` or want a badge header (e.g., license, build status).
```
