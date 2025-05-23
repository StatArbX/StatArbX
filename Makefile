.PHONY: setup run test freeze clean backtest

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

run:
	PYTHONPATH=src $(PYTHON) src/main.py

test:
	black .
	ruff check . --fix
	PYTHONPATH=src $(PYTHON) -m pytest tests/

backtest:
	PYTHONPATH=src $(PYTHON) src/core/backtest.py

plot:
	PYTHONPATH=src $(PYTHON) src/utils/plot_trades.py

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf __pycache__ .venv *.pyc *.log