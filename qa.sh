#!/bin/bash

set -e

virtualenv env
source env/bin/activate

pip install .[dev,test]

export DATA_DIR=tests/data

pyflakes valley tests
black --check valley tests
mypy valley tests
pytest -sv
