#!/bin/sh
# Runs every demo from a temp cwd; outputs saved to ../out. Venvs: sv (pyspark 4.2.0, pandas 2.3.3, pyarrow, delta-spark 4.4.1),
# misc (pandas for Q20), feast (Feast 0.67.0).
C=/home/user/case_studies/interviews/scratch/B4P09_Q19-27/code; O=/home/user/case_studies/interviews/scratch/B4P09_Q19-27/out
cd /tmp/claude-0/b9_q19_27
clean() { sed 's/\x1b\[[0-9;]*m//g'; }
python3 -I $C/q19_dlq.py > $O/q19.txt
/tmp/claude-0/b9p09/misc/bin/python -I $C/q20_rolling.py > $O/q20.txt
for q in q21_joins q22_udf q23_layout q23_delta q24_cache; do
  sv/bin/python -I $C/$q.py 2>/dev/null | clean > $O/$q.txt; done
python3 -I $C/q25_two_codebases.py > $O/q25.txt
python3 -I $C/q26_cdc.py > $O/q26.txt
/tmp/claude-0/b9p09/feast/bin/python -I $C/q27_online_lookup.py 2>/dev/null | clean > $O/q27.txt
