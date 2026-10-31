#!/bin/sh
# builds a throwaway venv in a temp dir, installs the package, runs tests and the CLI
set -e
SRC=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d); cd "$T"
cp -r "$SRC"/src "$SRC"/tests "$SRC"/pyproject.toml "$SRC"/make_data.py .
uv venv -q venv; uv pip install -q --python venv/bin/python -e ".[dev]"
venv/bin/python -I make_data.py data.csv
venv/bin/churn train --data data.csv --out model.joblib
venv/bin/churn train --data data.csv --out model2.joblib
venv/bin/python -I -m pytest -q -p no:cacheprovider
cp "$SRC"/bug_demo.py .; venv/bin/python -I bug_demo.py
