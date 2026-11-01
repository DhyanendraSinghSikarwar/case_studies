# Q25: register two versions, tag them, move the alias, print history from the client API.
import time, datetime as dt, mlflow
from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
mlflow.set_tracking_uri("sqlite:///mlflow.db")
c = MlflowClient(); NAME = "iris_gov"
X, y = load_iris(return_X_y=True, as_frame=True)
for C in (0.1, 5.0):
    m = LogisticRegression(C=C, max_iter=300).fit(X, y)
    with mlflow.start_run() as r:
        mlflow.log_param("C", C)
        mlflow.sklearn.log_model(m, name="model", signature=infer_signature(X, m.predict(X)), registered_model_name=NAME)
    v = c.search_model_versions(f"name='{NAME}'")[0].version      # newest first
    c.set_model_version_tag(NAME, v, "validation_status", "approved" if C == 5.0 else "pending")
    c.set_model_version_tag(NAME, v, "data_version", "md5:abc123")
    c.set_model_version_tag(NAME, v, "owner", "team-risk")
    time.sleep(1.1)
c.update_registered_model(NAME, description="Iris classifier (demo). Owner: team-risk.")

def move_alias(alias, to_version, who, why):
    """Audit trail is OUR job: the server stores the alias but not who moved it."""
    old = None
    try: old = c.get_model_version_by_alias(NAME, alias).version
    except Exception: pass
    c.set_registered_model_alias(NAME, alias, to_version)
    c.set_model_version_tag(NAME, to_version, "promoted_by", who)
    c.set_model_version_tag(NAME, to_version, "promoted_at", dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    c.set_model_version_tag(NAME, to_version, "promotion_note", f"{alias}: v{old or '-'} -> v{to_version}; {why}")

move_alias("champion", "1", "asha", "first release")
move_alias("champion", "2", "dev", "better CV score")
print("champion now v", c.get_model_version_by_alias(NAME, "champion").version, "| rollback = move it back:")
move_alias("champion", "1", "asha", "rollback, v2 latency regression")
print("champion after rollback: v", c.get_model_version_by_alias(NAME, "champion").version)

print("\nversion history")
for mv in [c.get_model_version(NAME, v) for v in ("1", "2")]:
    t = dt.datetime.fromtimestamp(mv.creation_timestamp / 1000, dt.timezone.utc).strftime("%H:%M:%S")
    print(f"v{mv.version} created {t}Z aliases={mv.aliases} run={mv.run_id[:8]}")
    for k in sorted(mv.tags): print(f"    {k} = {mv.tags[k]}")
rm = c.get_registered_model(NAME)
print("\nmodel description:", rm.description, "| aliases map:", rm.aliases)
