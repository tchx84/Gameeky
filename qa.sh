#!/bin/bash

set -e

pyflakes valley tests
black --check valley tests
mypy valley tests
pytest -sv