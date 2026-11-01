set -u; W=$1; SRC=$(cd "$(dirname "$0")" && pwd); rm -rf $W; mkdir -p $W/repo $W/remote; cd $W/repo
export PATH=/tmp/claude-0/ven/v/bin:$PATH MLFLOW_DISABLE_TELEMETRY=true MLFLOW_DISABLE_AGENT_HINT=1 WANDB_SILENT=true
git init -q -b main; git config user.email a@b.c; git config user.name t
cp $SRC/params.yaml $SRC/prepare.py $SRC/train.py .
dvc init -q; dvc remote add -d loc $W/remote >/dev/null; printf 'mlflow.db\nmlruns/\nwb/\n__pycache__/\n' > .gitignore
dvc stage add -q -n prepare -d prepare.py -o data.csv python prepare.py
dvc stage add -q -n train -d train.py -d data.csv -p train -o model.joblib -O MODEL_CARD.md -M metrics.json python train.py
git add -A; git commit -qm "pipeline"
echo "--- dvc repro (1)"; dvc repro 2>&1 | grep -E "Running|Updating|ERROR|Error" 
git add -A; git commit -qm "first run" ; dvc push 2>&1 | tail -1
echo "--- change a param, repro (2), diff"
sed -i 's/C: 1.0/C: 0.01/' params.yaml; dvc repro 2>&1 | grep -E "Running|ERROR"
dvc params diff 2>&1; dvc metrics diff 2>&1
echo "--- dvc dag"; dvc dag 2>&1 | head -12
echo "--- registry"; python -I -c "
import mlflow; mlflow.set_tracking_uri('sqlite:///mlflow.db'); c = mlflow.tracking.MlflowClient()
for v in c.search_model_versions(\"name='demo-clf'\"): print('demo-clf v'+str(v.version), 'aliases:', v.aliases)
print('alias candidate ->', c.get_model_version_by_alias('demo-clf','candidate').version)" 2>&1 | grep -v INFO
echo "--- wandb offline run dirs"; ls wb/wandb | sed -E 's/offline-run-[0-9_]+-/offline-run-<ts>-/'
echo "--- model card"; cat MODEL_CARD.md
