import os, pytest
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"
import mlflow
from mlflow import MlflowClient
from cas_promote import promote_forward, current


@pytest.fixture()
def client(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    c = MlflowClient(uri, registry_uri=uri)
    c.create_registered_model("churn")
    for i in range(3):                                   # three versions, no artifacts needed
        c.create_model_version("churn", source=f"{tmp_path}/fake{i}", run_id=None)
    return c


def test_forward_ok(client):
    assert promote_forward(client, "churn", 1)[0]
    assert promote_forward(client, "churn", 3)[0]
    assert current(client, "churn") == 3


def test_stale_run_cannot_move_backwards(client):
    promote_forward(client, "churn", 3)                  # the newer run finished first
    ok, msg = promote_forward(client, "churn", 2)        # the older run finishes late
    assert not ok and "older" in msg
    assert current(client, "churn") == 3


def test_expected_mismatch_refused(client):
    promote_forward(client, "churn", 1)
    promote_forward(client, "churn", 2)                  # someone else moved it
    ok, msg = promote_forward(client, "churn", 3, expected=1)
    assert not ok and "moved under us" in msg
    assert current(client, "churn") == 2


def test_noop(client):
    promote_forward(client, "churn", 2)
    assert promote_forward(client, "churn", 2)[1].startswith("NO-OP")
