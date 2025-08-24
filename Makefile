PY=python
PIP=pip

.PHONY: setup test run chat clean help

setup:
	$(PY) -m venv .venv
	.venv/Scripts/activate && $(PIP) install -r requirements.txt

test:
	pytest tests/test_integration.py -v
	pytest tests/test_real_tools.py -v

test-integration:
	pytest tests/test_integration.py -v

test-tools:
	pytest tests/test_real_tools.py -v

run:
	$(PY) main.py "What is 12.5% of 243?"

chat:
	$(PY) chat.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache

help:
	@echo "Available commands:"
	@echo "  setup      - Create venv and install dependencies"
	@echo "  test       - Run all tests"
	@echo "  test-tools - Run tool tests without API calls"
	@echo "  run        - Run single query example"
	@echo "  chat       - Start interactive chat mode"
	@echo "  clean      - Remove cache files"
	@echo "  help       - Show this help"