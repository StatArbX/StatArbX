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

3. **ML-Based Profitability Scoring**
   - Train a regression model using historical pair features and resulting PnL
   - Predict expected profitability scores for each pair
   - Retain only top-scoring pairs for backtesting
   - Current model: RandomForestRegressor using features like:
	   •	Correlation
	   •	Cointegration p-value
	   •	Mean half-life
	   •	Price ratio volatility

4. **Spread Computation**
   - Use linear regression to compute spread between each pair
   - Calculate Z-score for identifying trading opportunities
   - Define entry and exit thresholds

5. **Backtesting Engine**
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
This will:

* Executes the full pipeline:
	*	Load data
	*	Select pairs
	*	Score using ML
	*	Backtest top pairs
	*	Output metrics and charts
---

## 🧪 Running Backtesting
```bash
make backtest
```

This will:

* Load tickers from data/tickers.txt
* Download historical stock data using yfinance
* Select statistically cointegrated pairs
* Simulate trades based on z-score thresholds
* Output metrics like:
   * Number of trades
   * Total PnL
   * Win rate		

Make sure you have a valid tickers.txt file inside the data/ folder with one ticker per line.

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

