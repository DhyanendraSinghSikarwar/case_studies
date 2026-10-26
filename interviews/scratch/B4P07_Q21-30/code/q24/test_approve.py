import os

import mlflow
import pytest
from mlflow import MlflowClient

from approve import PromotionRefused, approve, promote

os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"


@pytest.fixture
def reg(tmp_path):
    uri = f"sqlite:///{tmp_path}/m.db"
    mlflow.set_tracking_uri(uri)
    mlflow.set_registry_uri(uri)
    c = MlflowClient(uri, uri)
    c.create_registered_model("churn")
    mv = c.create_model_version("churn", source="file:///tmp/none", tags={"author": "asha"})
    return c, mv.version


def test_author_cannot_approve(reg):
    c, v = reg
    with pytest.raises(PromotionRefused, match="is the author"):
        approve(c, "churn", v, "asha", "https://ci.example/report/1", 101)
    assert "approved_by" not in c.get_model_version("churn", v).tags


def test_other_person_approves_and_promotes(reg):
    c, v = reg
    tags = approve(c, "churn", v, "ravi", "https://ci.example/report/1", 101)
    assert tags["approved_by"] == "ravi"
    promote(c, "churn", v)
    assert c.get_model_version_by_alias("churn", "champion").version == v


def test_promote_without_approval_refused(reg):
    c, v = reg
    with pytest.raises(PromotionRefused, match="approved_by"):
        promote(c, "churn", v)


def test_break_glass_still_needs_second_person_and_leaves_a_mark(reg):
    c, v = reg
    with pytest.raises(PromotionRefused):
        approve(c, "churn", v, "asha", None, 7, break_glass_reason="INC-42")
    tags = approve(c, "churn", v, "ravi", None, 7, break_glass_reason="INC-42")
    assert tags["break_glass"] == "true"
