.PHONY: all start-server install-dev docs format

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
LINT_PATHS = src/ setup.py
ISORT_PARAMS = --ignore-whitespace --settings-path ./ $(LINT_PATHS)

format: isort black

black:
	black $(BLACK_CHECK_PARAMS) $(LINT_PATHS)

isort:
	isort $(ISORT_PARAMS) $(ISORT_CHECK_PARAMS)

install-dev:
	pip install -r requirements-dev.txt; python setup.py develop

docs: export RAIDEN_PAYWALL_SETTINGS=${ROOT_DIR}/default.cfg
docs:
	# rm -rf docs/api
	# SPHINX_APIDOC_OPTIONS='members,special-members,private-members,undoc-members,show-inheritance' sphinx-apidoc -o docs/api/ intellprice
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

start-server: export FLASK_APP=${ROOT_DIR}/main.py
start-server: export RAIDEN_PAYWALL_SETTINGS=${ROOT_DIR}/default.cfg
start-server:
	gunicorn -w 4 -b localhost:5000 -c ./src/raiden_paywall/config.py main:app
