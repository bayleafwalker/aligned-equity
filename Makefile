SHELL := /usr/bin/bash

PYTHON := $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else command -v python3 || command -v python; fi)
PYTEST := $(PYTHON) -m pytest
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy

.PHONY: lint typecheck test validate hla-contract-check verify-fast

lint:
	$(RUFF) check .

typecheck:
	$(MYPY) apps packages tests

test:
	$(PYTEST) -q

validate:
	$(PYTHON) -m apps.validator.main

hla-contract-check:
	$(PYTHON) -m apps.validator.hla_contract

verify-fast: lint typecheck test validate hla-contract-check
