.PHONY: install

SHELL := /bin/bash
.ONESHELL:
.DEFAULT_GOAL := run

PYENV_ROOT = $(HOME)/.pyenv
PYTHON_VERSION ?= 3.9.16
VENV = .venv
PYTHON = ./$(VENV)/bin/python3
PIP = ./$(VENV)/bin/pip


pyenv:
	@export PYENV_ROOT=$(PYENV_ROOT)
	@bash ./setup/installation/setup_pyenv.sh
	@eval "$(pyenv init -)"
	@pyenv install -s $(PYTHON_VERSION)
	@pyenv local $(PYTHON_VERSION)
	
venv/bin/activate: pyenv requirements
	@echo "Using $(shell python -V)"
ifeq ($(COPY_VENV), true)
	@echo "Installing venv with copies instead of symlinks"
	@python3 -m venv $(VENV) --copies --clear
else
	@python3 -m venv $(VENV)
endif
	@chmod +x $(VENV)/bin/activate
	@source ./$(VENV)/bin/activate
	@$(PIP) install --upgrade -q pip==23.0 setuptools
	@echo "BUILD DEPENDENCIES INSTALLED"
	@$(PIP) install -q -r requirements/requirements.txt
	@echo "CPU DEPENDENCIES INSTALLED"

venv: venv/bin/activate
	@source ./$(VENV)/bin/activate
	@echo "VIRTUAL ENVIRONMENT LOADED"

install: venv



