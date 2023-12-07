#!/bin/bash

set -e

virtualenv env
source env/bin/activate

pip install .[dev,test]

export DATA_DIR=tests/data

pyflakes gameeky tests examples
black --check gameeky tests examples
mypy gameeky tests examples
pytest -sv
