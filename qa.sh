#!/bin/bash

set -e

virtualenv env
source env/bin/activate

pip install .[dev,test]

export DATA_DIR=tests/data

pyflakes valley tests examples
black --check valley tests examples
mypy valley tests examples
pytest -sv
