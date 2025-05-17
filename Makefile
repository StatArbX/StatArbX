.PHONY: setup run test freeze clean

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
	PYTHONPATH=src $(PYTHON) -m pytest tests/

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf __pycache__ .venv *.pyc *.log
