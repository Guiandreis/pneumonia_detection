.PHONY: install aws

SHELL := /bin/bash
.ONESHELL:
.DEFAULT_GOAL := run

PYENV_ROOT = $(HOME)/.pyenv
PYTHON_VERSION ?= 3.9.16
VENV = .venv
PYTHON = ./$(VENV)/bin/python3
PIP = ./$(VENV)/bin/pip
AWS?=true

pyenv:
	@export PYENV_ROOT=$(PYENV_ROOT)
	@bash ./setup/installation/setup_pyenv.sh
	@export PATH=$(PYENV_ROOT)/bin:$(PATH)
	@eval "$(pyenv init -)"
	@pyenv install -s $(PYTHON_VERSION)
	@pyenv local $(PYTHON_VERSION)

venv/bin/activate: pyenv requirements
	@echo "Using $(shell python3 -V)"
ifeq ($(COPY_VENV), true)
	@echo "Installing venv with copies instead of symlinks"
	@python3 -m venv $(VENV) --copies --clear
else
	@python3 -m venv $(VENV)
endif
	@chmod +x $(VENV)/bin/activate
	@source ./$(VENV)/bin/activate

venv: venv/bin/activate
	@source ./$(VENV)/bin/activate
	@echo "VIRTUAL ENVIRONMENT LOADED $(VENV)"

install: venv

ifeq ($(AWS),true)

	@echo "entrou aws"
	@bash ./setup/installation/setup_aws.sh
	@bash ./setup/installation/setup_s3.sh


endif