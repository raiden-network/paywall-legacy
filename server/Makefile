ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

start-server: export FLASK_APP=${ROOT_DIR}/src/raiden_paywall/main.py
start-server: export RAIDEN_PAYWALL_SETTINGS=${ROOT_DIR}/default.cfg
start-server:
	flask run

install-dev:
	pip install -r requirements.txt; python setup.py develop
