.PHONY: setup run test freeze clean backtest

PYTHON := .venv/bin/python
PIP := .venv/bin/pip

setup:
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

run:
	@echo "Nothing to run yet. Add your entry point to run this."

test:
	black .
	ruff check . --fix
	PYTHONPATH=src $(PYTHON) -m pytest tests/

backtest:
	PYTHONPATH=src $(PYTHON) src/core/backtest.py

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf __pycache__ .venv *.pyc *.log