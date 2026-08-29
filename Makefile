SHELL := /usr/bin/bash

PYTHON := $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; else command -v python3 || command -v python; fi)
PYTEST := $(PYTHON) -m pytest
RUFF := $(PYTHON) -m ruff
MYPY := $(PYTHON) -m mypy
WORKFLOW_HELPER := ./tools/workflow.sh

ITEM ?=
SPRINT_ID ?=
CLAIM_ID ?=
CLAIM_TOKEN ?=
CLAIM_TTL ?=
ACTOR ?=
PY_FILES ?=
TESTS ?=
CANDIDATE ?=
CATEGORY ?=
BODY ?=
TITLE ?=
TAGS ?=
COORDINATION ?=

export ITEM SPRINT_ID CLAIM_ID CLAIM_TOKEN CLAIM_TTL ACTOR PY_FILES TESTS CANDIDATE CATEGORY BODY TITLE TAGS COORDINATION
export SPRINTCTL_INSTANCE_ID SPRINTCTL_RUNTIME_SESSION_ID CODEX_THREAD_ID

.PHONY: lint typecheck test validate hla-contract-check verify-fast \
	sprint-resume claim-recover claim-heartbeat item-verify-auth snapshot-refresh knowledge-publish

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

sprint-resume:
	$(WORKFLOW_HELPER) sprint-resume

claim-recover:
	$(WORKFLOW_HELPER) claim-recover

claim-heartbeat:
	$(WORKFLOW_HELPER) claim-heartbeat

item-verify-auth:
	$(WORKFLOW_HELPER) item-verify-auth

snapshot-refresh:
	$(WORKFLOW_HELPER) snapshot-refresh

knowledge-publish:
	$(WORKFLOW_HELPER) knowledge-publish
