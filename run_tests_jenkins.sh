#! /usr/bin/env bash 
set -e

# Load previously installed climada_jenkins environment
source activate climada_env

# install validation libraries
pip install coverage

# run all climada tests
PYTHONPATH=. python -m coverage run --parallel-mode --concurrency=multiprocessing unit_tests.py
PYTHONPATH=. python -m coverage run --parallel-mode --concurrency=multiprocessing integ_tests.py
PYTHONPATH=. python -m coverage combine

# analize coverage
python -m coverage xml -o coverage.xml
python -m coverage html -d coverage

# run static code analysis
pylint -ry --rcfile=./pylint_conf.rc climada > pylint.log || true

