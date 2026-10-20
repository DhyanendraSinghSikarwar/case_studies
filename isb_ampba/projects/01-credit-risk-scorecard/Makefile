PY ?= python
.PHONY: setup data train evaluate app test lint all
setup:
	$(PY) -m pip install -r requirements.txt && $(PY) -m pip install -e .
data:
	$(PY) tasks.py data
train:
	$(PY) tasks.py train
evaluate:
	$(PY) tasks.py evaluate
app:
	$(PY) tasks.py app
test:
	$(PY) tasks.py test
lint:
	$(PY) tasks.py lint
all:
	$(PY) tasks.py all
