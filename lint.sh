#!/bin/bash

# Run Black for code formatting
echo "Running Black..."
poetry run black photosort/

# Run Pylint
echo "Running Pylint..."
PYTHONPATH=$(pwd) poetry run pylint photosort/

# Run Mypy for type checking
echo "Running Mypy..."
poetry run mypy --explicit-package-bases photosort/

echo "Linting and type checking completed successfully!"
