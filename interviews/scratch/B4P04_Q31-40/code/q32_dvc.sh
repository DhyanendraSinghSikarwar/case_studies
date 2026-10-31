#!/bin/bash
# Reproduce DVC debugging cases 1, 2, 3 in a temp repo. Usage: q32_dvc.sh WORKDIR
set -u
W=$1; rm -rf "$W"; mkdir -p "$W/repo" "$W/remote"; cd "$W/repo"
git init -q -b main; git config user.email a@b.c; git config user.name t
dvc init -q; git commit -qm init
printf 'a,b\n1,2\n3,4\n' > data.csv
dvc remote add -d loc "$W/remote" >/dev/null
dvc add data.csv >/dev/null
git add -A; git commit -qm "data"
echo "=== CASE 1: dvc pull when the remote never received the data (forgot dvc push)"
rm -rf data.csv .dvc/cache
dvc pull 2>&1 | tail -6
echo "--- confirm: what does the remote hold?"; find "$W/remote" -type f | wc -l
echo "--- fix: push from a machine that has the cache"
printf 'a,b\n1,2\n3,4\n' > data.csv; dvc add data.csv >/dev/null; dvc push 2>&1 | tail -1
rm -rf data.csv .dvc/cache; dvc pull 2>&1 | tail -1

echo; echo "=== CASE 2: dvc repro re-runs although nothing changed"
mkdir -p feats; echo x > feats/f1.txt
printf 'lr: 0.1\nnoise: 1\n' > params.yaml
printf 'import yaml\nlr = yaml.safe_load(open("params.yaml"))["lr"]\nopen("out.txt", "w").write(str(lr))\n' > prep.py
echo "--- cause A: whole params.yaml listed as a plain dependency"
dvc stage add -q -n prep -d prep.py -d params.yaml -o out.txt python prep.py
dvc repro 2>&1 | grep -E "Running|up to date"
sed -i 's/noise: 1/noise: 2/' params.yaml         # change a key the script never reads
dvc repro 2>&1 | grep -E "Running|up to date"
echo "--- fix: depend on the keys the stage reads (-p lr)"
dvc stage add -q -f -n prep -d prep.py -p lr -o out.txt python prep.py
dvc repro 2>&1 | grep -E "Running|up to date"
sed -i 's/noise: 2/noise: 3/' params.yaml
dvc repro 2>&1 | grep -E "Running|up to date"
echo "--- cause B: dvc.lock was not committed or was deleted"
cp dvc.lock /tmp/lock.bak; rm dvc.lock
dvc status 2>&1 | head -3
dvc repro 2>&1 | head -3
echo "--- cause C: --always-changed on the stage"
dvc stage add -q -f -n prep -d prep.py -p lr -o out.txt --always-changed python prep.py
dvc repro 2>&1 | grep -E "Running"; dvc repro 2>&1 | grep -E "Running"
dvc stage add -q -f -n prep -d prep.py -p lr -o out.txt python prep.py; dvc repro 2>&1 | grep -E "Running|up to date"; dvc repro 2>&1 | grep -E "Running|up to date"
git add -A; git commit -qm pipeline

echo; echo "=== CASE 3: conflict in dvc.lock"
git checkout -qb exp1; sed -i 's/lr: 0.1/lr: 0.2/' params.yaml; dvc repro >/dev/null 2>&1; git add -A; git commit -qm exp1
git checkout -q main; git checkout -qb exp2; sed -i 's/lr: 0.1/lr: 0.3/' params.yaml; dvc repro >/dev/null 2>&1; git add -A; git commit -qm exp2
git merge exp1 2>&1 | tail -3
echo "--- markers in dvc.lock:"; grep -nE '^(<<<<<<<|=======|>>>>>>>)' dvc.lock
echo "--- dvc status:"; dvc status 2>&1 | tail -4
echo "--- fix: abort, merge again, take either lock, re-run, commit"
git merge --abort
git merge exp1 -q -X theirs -m "merge exp1" 2>&1 | tail -1
dvc repro 2>&1 | grep -E "Running|up to date"; dvc status 2>&1 | head -2
