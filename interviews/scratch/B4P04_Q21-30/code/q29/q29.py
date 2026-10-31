# Q29: generate a model card (markdown) from MLflow run + registry data, log it back as an artifact.
import json, mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
mlflow.set_tracking_uri("sqlite:///mlflow.db"); c = MlflowClient(); NAME = "iris_card"

# --- train + log (slice = petal length bucket) ---
X, y = load_iris(return_X_y=True, as_frame=True)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
m = LogisticRegression(C=1.0, max_iter=300).fit(Xtr, ytr)
pred = m.predict(Xte)
with mlflow.start_run() as run:
    mlflow.log_params({"C": 1.0, "max_iter": 300, "test_size": 0.3, "seed": 0})
    mlflow.log_metric("test_acc", accuracy_score(yte, pred))
    short = Xte["petal length (cm)"] < 3
    mlflow.log_metric("acc_slice_short_petal", accuracy_score(yte[short], pred[short]))
    mlflow.log_metric("acc_slice_long_petal", accuracy_score(yte[~short], pred[~short]))
    mlflow.set_tags({"data_version": "md5:abc123 (demo)", "git_sha": "deadbeef (demo)", "owner": "team-risk"})
    mlflow.sklearn.log_model(m, name="model", signature=infer_signature(Xtr, m.predict(Xtr)), registered_model_name=NAME)
c.set_registered_model_alias(NAME, "champion", 1)

# --- build the card from stored facts, never from memory ---
def card(name, alias):
    mv = c.get_model_version_by_alias(name, alias)
    r = c.get_run(mv.run_id)
    sig = mlflow.models.get_model_info(f"models:/{name}@{alias}").signature.to_dict()
    L = [f"# Model card: {name} (v{mv.version}, alias {alias})", "",
         "## Intended use", "- Classify iris species from 4 measurements. Demo only, not for botanical decisions. (hand-written field)", "",
         "## Training data", f"- data_version: {r.data.tags.get('data_version', 'MISSING')}", f"- code: git {r.data.tags.get('git_sha', 'MISSING')}", "",
         "## Parameters"] + [f"- {k}: {v}" for k, v in sorted(r.data.params.items())] + ["", "## Metrics", "| metric | value |", "|---|---|"]
    L += [f"| {k} | {v:.3f} |" for k, v in sorted(r.data.metrics.items())]
    L += ["", "## Inputs", "| name | type |", "|---|---|"] + [f"| {i['name']} | {i['type']} |" for i in json.loads(sig["inputs"])]
    L += ["", "## Limitations", "- Only 150 rows; slice metrics rest on few test rows, check the counts before trusting them. (hand-written field)",
          f"- Owner: {r.data.tags.get('owner', 'MISSING')}", f"- Run: {mv.run_id}", ""]
    missing = [l for l in L if "MISSING" in l]
    return "\n".join(L), missing

text, missing = card(NAME, "champion")
print(text); print("fields missing:", missing or "none")
with mlflow.start_run(run_id=c.get_model_version_by_alias(NAME, "champion").run_id):
    mlflow.log_text(text, "MODEL_CARD.md")
open("MODEL_CARD.md", "w").write(text)
c.set_model_version_tag(NAME, "1", "model_card", "artifact: MODEL_CARD.md on the training run")
print("slice sizes in the test set: short petal =", int(short.sum()), ", long petal =", int((~short).sum()))
