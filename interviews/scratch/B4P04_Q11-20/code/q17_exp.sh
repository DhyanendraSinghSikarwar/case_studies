git init -q . && dvc init -q
cp /home/user/case_studies/interviews/scratch/B4P04_Q11-20/code/q17_train.py train.py
printf 'train:\n  C: 1.0\n' > params.yaml
dvc stage add -q -n train -d train.py -p train.C -M metrics.json python train.py
git add -A; git commit -qm base
dvc repro >/dev/null 2>&1; git add -A; git commit -qm "baseline run"
echo "=== two experiments with -S"
dvc exp run -S train.C=0.01 -n c-small 2>&1 | grep -e Experiment -e "exp-" | head -3
dvc exp run -S train.C=100 -n c-big 2>&1 | grep -e Experiment | head -3
echo "=== queue two more, then run them"
dvc exp run --queue -S train.C=0.1 -n q-01 2>&1 | grep -i queued
dvc exp run --queue -S train.C=10 -n q-10 2>&1 | grep -i queued
dvc exp run --run-all 2>&1 | grep -ie "experiment results" -e error | head
echo "=== dvc exp show"; dvc exp show --no-pager --md 2>&1
echo "=== dvc exp diff c-small c-big"; dvc exp diff c-small c-big 2>&1
echo "=== git sees nothing: branch still clean, refs hidden"; git status --short; git branch; git for-each-ref | awk '{print $3}' | head -5
echo "=== promote: apply c-small, then commit"
dvc exp apply c-small 2>&1 | tail -1; git diff --stat; git commit -qam "adopt C=0.01"; git log --oneline | head -3
echo "=== or branch from another experiment"
dvc exp branch c-big try-big 2>&1; git branch
