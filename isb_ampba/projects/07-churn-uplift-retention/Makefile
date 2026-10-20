PY ?= python
export PYTHONPATH := src

.PHONY: setup data train evaluate app test lint all

setup:
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -e .

data:
	$(PY) -m churnx.data

train:
	$(PY) -m churnx.train

evaluate:
	$(PY) analysis/run_analysis.py

app:
	$(PY) -m streamlit run app/streamlit_app.py

test:
	$(PY) -m pytest -q

lint:
	$(PY) -m ruff check .

all: data train evaluate lint test
