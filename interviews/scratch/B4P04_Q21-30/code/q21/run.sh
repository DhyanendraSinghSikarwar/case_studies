set -e
source "$(dirname "$0")/../env.sh"
W=$(mktemp -d /tmp/claude-0/b4q21.XXXX); cp "$(dirname "$0")"/{MLproject,train.py} $W/; cd $W
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
mlflow --version
mlflow run . --env-manager local --experiment-name proj -P C=0.5 2>&1 | grep -v '^$' | tail -8
python3 -I - <<'P'
import mlflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
df = mlflow.search_runs(experiment_names=["proj"])
r = df.iloc[0]
print(df.shape[0], "run;", "status", r["status"])
print({k: r[k] for k in ["params.C","params.max_iter","metrics.test_acc"]})
print(sorted(c for c in df.columns if c.startswith("tags.mlflow")))
print("source.name:", r["tags.mlflow.source.name"], "| source.type:", r["tags.mlflow.source.type"])
P
