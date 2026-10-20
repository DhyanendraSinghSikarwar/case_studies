# make alternative: python tasks.py <target>
PY ?= python
export PYTHONPATH := src

.PHONY: setup data train evaluate app test lint all
setup:
	$(PY) -m pip install -r requirements.txt
data:
	$(PY) -m promo.data
train:
	$(PY) -m promo.train
evaluate:
	$(PY) analysis/run_analysis.py
app:
	$(PY) -m streamlit run app/streamlit_app.py
test:
	$(PY) -m pytest -q
lint:
	$(PY) -m ruff check .
all: data train evaluate test lint
