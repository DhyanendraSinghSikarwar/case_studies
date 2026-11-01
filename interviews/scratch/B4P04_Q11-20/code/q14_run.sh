set -e
P=/home/user/case_studies/interviews/scratch/B4P04_Q11-20/code/q14_proj
git init -q . && dvc init -q && cp $P/train.py $P/lineage.py .
python -I -c "
import numpy as np, pandas as pd
r = np.random.default_rng(0); x = r.normal(size=(300, 2))
y = (x[:,0] + 0.5*x[:,1] + r.normal(scale=0.7, size=300) > 0).astype(int)
pd.DataFrame({'x1': x[:,0], 'x2': x[:,1], 'y': y}).to_csv('data.csv', index=False)"
printf 'train:\n  C: 1.0\n' > params.yaml
dvc add data.csv >/dev/null 2>&1
dvc stage add -q -n train -d train.py -d data.csv -p train.C -M metrics.json python train.py
cat dvc.yaml
printf 'mlflow.db\nmlruns/\n' >> .gitignore
git add -A && git commit -qm "data v1 + pipeline"
echo "=== dvc repro"; dvc repro 2>&1 | grep -v -e '^$' -e 'git add' -e autostage -e 'To track' | tail -8
echo "=== dvc.lock"; cat dvc.lock
git add -A && git commit -qm "first model"
echo "=== mlflow run (search_runs)"
python -I -c "
import mlflow; mlflow.set_tracking_uri('sqlite:///mlflow.db')
df = mlflow.search_runs(experiment_names=['dvc-plus-mlflow'])
r = df.iloc[0]
for k in ['params.C','metrics.cv_acc','tags.git_sha','tags.git_dirty','tags.dvc_data_md5']: print(k, '=', r[k])"
echo "=== lineage for churn v1"
python -I lineage.py churn 1
echo "=== change params -> new model version"
sed -i 's/C: 1.0/C: 0.1/' params.yaml; dvc repro 2>&1 | grep -e Running -e Updating; git add -A; git commit -qm "C=0.1"
python -I lineage.py churn 2
