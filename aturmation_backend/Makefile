.PHONY: install test clean develop serve initdb

# Variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

# Windows-specific settings
ifeq ($(OS),Windows_NT)
	VENV = venv
	PYTHON = $(VENV)\Scripts\python
	PIP = $(VENV)\Scripts\pip
	PYTEST = $(VENV)\Scripts\pytest
endif

# Install dependencies
install: $(VENV)
	$(PIP) install -e .
	$(PIP) install -e ".[testing]"

# Install in development mode
develop: $(VENV)
	$(PIP) install -e .
	$(PIP) install -e ".[testing]"

# Create virtual environment
$(VENV):
	python -m venv $(VENV)

# Run tests
test:
	$(PYTEST)

# Run tests with coverage
coverage:
	$(PYTEST) --cov=aturmation --cov-report=term-missing

# Initialize the database
initdb:
	$(PYTHON) -m aturmation.scripts.initialize_db development.ini

# Serve the application
serve:
	$(PYTHON) main.py

# Clean up generated files
clean:
	rm -rf $(VENV) *.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
