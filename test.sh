#!/bin/bash

# Run Tests with Coverage
echo "Running Tests with Coverage..."
poetry run python -m pytest -vv --cov=photosort --cov-report=term-missing --cov-report=html photosort/tests/
echo "Open htmlcov/index.html to view the full coverage report."