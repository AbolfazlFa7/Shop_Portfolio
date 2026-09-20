SHELL := /bin/sh

PROJECT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null || pwd)
SRC_DIR := $(PROJECT_ROOT)/src

# Run a command from the src directory.
define run_in_src
	cd "$(SRC_DIR)" && $(1)
endef

.PHONY: init migrate run test lint lint-fix seed shell

init:
	$(call run_in_src,uv sync)

migrate:
	$(call run_in_src,uv run manage.py migrate)

run:
	$(call run_in_src,uv run manage.py runserver)

test:
	$(call run_in_src,uv run pytest)

lint:
	$(call run_in_src,uv run ruff check)
	$(call run_in_src,uv run ruff format --check)

lint-fix:
	$(call run_in_src,uv run ruff check --fix --unsafe-fixes)
	$(call run_in_src,uv run ruff format)

seed:
	$(call run_in_src,uv run manage.py seed --scale medium)

shell:
	$(call run_in_src,uv run manage.py shell)