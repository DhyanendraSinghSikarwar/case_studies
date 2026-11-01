import json, pytest
from mlflow import MlflowClient
from envpromo import promote, PromotionError

@pytest.fixture
def setup(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    c = MlflowClient(tracking_uri=uri, registry_uri=uri)
    c.create_registered_model("churn")
    for _ in range(2):
        c.create_model_version("churn", source=str(tmp_path))
    return c, str(tmp_path / "ledger.jsonl")

def test_cannot_skip_staging(setup):
    c, led = setup
    with pytest.raises(PromotionError, match="never reached staging"):
        promote(c, "churn", 1, "champion", "ci", led)

def test_in_order_then_idempotent(setup):
    c, led = setup
    assert promote(c, "churn", 1, "staging", "ci", led) == "moved"
    assert promote(c, "churn", 1, "champion", "ci", led) == "moved"
    assert promote(c, "churn", 1, "champion", "ci", led) == "noop"
    rows = [json.loads(l) for l in open(led)]
    assert [(r["env"], r["version"]) for r in rows] == [("staging", "1"), ("champion", "1")]

def test_unknown_version_and_env(setup):
    c, led = setup
    with pytest.raises(PromotionError):
        promote(c, "churn", 9, "staging", "ci", led)
    with pytest.raises(PromotionError):
        promote(c, "churn", 1, "prod", "ci", led)
