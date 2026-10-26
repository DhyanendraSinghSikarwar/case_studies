R=$(mktemp -d /tmp/q20remote.XXXX)
git init -q -b main . && dvc init -q && dvc remote add -d loc $R -q
python -I -c "
import numpy as np; r=np.random.default_rng(0); x=r.normal(size=(200,2)); y=(x[:,0]+r.normal(scale=.8,size=200)>0).astype(int)
open('data.csv','w').write('x1,x2,y\n'+'\n'.join(f'{a:.4f},{b:.4f},{c}' for (a,b),c in zip(x,y))+'\n')"
printf 'train:\n  C: 1.0\n' > params.yaml
cat > train.py <<'P'
import json, yaml, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
C = yaml.safe_load(open("params.yaml"))["train"]["C"]; d = pd.read_csv("data.csv")
json.dump({"acc": round(float(cross_val_score(LogisticRegression(C=C), d[["x1","x2"]], d.y, cv=5).mean()), 4)}, open("metrics.json", "w"))
P
dvc add data.csv >/dev/null 2>&1
dvc stage add -q -n train -d train.py -d data.csv -p train.C -M metrics.json python train.py
dvc repro >/dev/null 2>&1; git add -A; git commit -qm base; dvc push 2>&1 | tail -1
echo "=== branch data-v2: new rows in data.csv"
git checkout -q -b data-v2; echo "0.1000,0.2000,1" >> data.csv; dvc repro 2>&1 | grep Running; git add -A; git commit -qm "more data"; dvc push 2>&1 | tail -1
echo "--- what the PR shows (git diff main..data-v2, hashes only):"; git diff main..data-v2 --stat; git diff main..data-v2 -U0 -- data.csv.dvc | grep -v -e '^diff' -e '^index'
git checkout -q main; git checkout -q -b params-c01; sed -i 's/C: 1.0/C: 0.1/' params.yaml; dvc repro 2>&1 | grep Running; git add -A; git commit -qm "C=0.1"
git checkout -q main; git merge -q data-v2 -m "merge data-v2" 2>&1 | tail -1
echo "=== merge params-c01 into main"
git merge params-c01 2>&1 | grep -i conflict
echo "--- conflict markers in dvc.lock:"; git diff --name-only --diff-filter=U; grep -n -e '<<<<<<<' -e '=======' -e '>>>>>>>' dvc.lock
echo "=== resolve: take one side of the generated files, let DVC recompute them"
git checkout --ours dvc.lock metrics.json; dvc repro 2>&1 | grep -v -e "^$" -e autostage -e "git add" -e "To track" -e "To enable" -e "dvc push"
git add dvc.lock metrics.json; git commit -qm "merge params-c01; dvc repro"
python -I -c "
import yaml; l=yaml.safe_load(open('dvc.lock'))['stages']['train']
print('lock params:', l['params']['params.yaml'], '| data md5:', [d['md5'] for d in l['deps'] if d['path']=='data.csv'][0])"
grep md5 data.csv.dvc; tail -1 data.csv
echo "=== CI check: someone commits a data change but forgets dvc push"
echo "0.3,0.3,0" >> data.csv; dvc add data.csv >/dev/null 2>&1; git add -A; git commit -qm "forgot to push"
dvc status -c; echo "exit=$?"
dvc status -c --json; echo "exit=$?"
dvc push 2>&1 | tail -1
dvc status -c; echo "exit=$?"
