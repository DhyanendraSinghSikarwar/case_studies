#!/bin/bash
R=/home/user/case_studies/interviews/scratch/B4P08_Q24-34
PY=/tmp/claude-0/b8p08/v/bin/python
mkdir -p $R/out
r(){ n=$1; shift; (cd $R/code/$n && "$@") > $R/out/$n.txt 2>&1; }
r q24 $PY -I cbpe_lite.py
r q25 $PY -I label_budget.py
r q26 $PY -I burn_rate.py
r q27 bash -c 'python3 -I validate_catalogue.py catalogue.yaml catalogue_bad.yaml; python3 -I check_routing.py'
r q28 $PY -I fairness.py
r q29 $PY -I safe_log.py
r q30 bash -c 'python3 -I check_files.py; python3 -I for_logic.py'
r q31 $PY -I constraints_check.py
r q32 $PY -I batch_validate.py
r q33 $PY -I loop.py
r q34 $PY -I incident.py
