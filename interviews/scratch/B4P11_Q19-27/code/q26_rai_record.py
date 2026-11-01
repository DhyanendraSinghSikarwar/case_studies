"""Q26: record RAI evidence as flat string tags on an Azure ML Model (offline) and validate the schema with pydantic.
No dashboard was generated; the numbers in the sample are made up for the schema test."""
import warnings; warnings.filterwarnings("ignore")
import importlib.metadata as md, json
from typing import Literal
from pydantic import BaseModel, Field, ValidationError, field_validator
from azure.ai.ml.entities import Model
print("azure-ai-ml", md.version("azure-ai-ml"), "| pydantic", md.version("pydantic"))

class RaiEvidence(BaseModel):
    model_name: str
    model_version: str
    dashboard_uri: str = Field(pattern=r"^(azureml|gs|https)://")   # where the full artefact lives
    protected_attribute: str                                           # e.g. gender (only if legally and ethically usable)
    fairness_metric: Literal["demographic_parity_difference", "equalized_odds_difference"]
    fairness_value: float = Field(ge=0, le=1)
    threshold: float = Field(gt=0, le=1)
    explainability_method: Literal["shap", "mimic", "integrated_gradients", "sampled_shapley", "none"]
    reviewer: str
    reviewed_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    limitations: str = Field(min_length=20)                            # what the evidence does NOT prove

    @field_validator("explainability_method")
    @classmethod
    def not_none(cls, v):
        if v == "none": raise ValueError("explainability_method 'none' needs a written exception, not a tag")
        return v
    def to_tags(self) -> dict[str, str]:                               # registry tags are flat strings
        return {f"rai.{k}": str(v) for k, v in self.model_dump().items() if k not in ("model_name", "model_version")}
    @property
    def passed(self): return self.fairness_value <= self.threshold

good = dict(model_name="credit-risk", model_version="7", dashboard_uri="azureml://registries/r/rai/dash1",
            protected_attribute="gender", fairness_metric="demographic_parity_difference", fairness_value=0.04,
            threshold=0.05, explainability_method="shap", reviewer="model-risk@example.com", reviewed_on="2026-10-20",
            limitations="Tested on 2025 applicant data only; no intersectional slices.")
ev = RaiEvidence(**good)
m = Model(name=ev.model_name, version=ev.model_version, path="./model", tags=ev.to_tags())
print("tags on Model entity:", len(m.tags), "e.g.", {k: m.tags[k] for k in list(m.tags)[:3]})
print("gate passed:", ev.passed, "(a pass is a threshold check, not proof of fairness)")
for label, patch in [("fairness out of range", {"fairness_value": 1.7}), ("method none", {"explainability_method": "none"}),
                     ("short limitations", {"limitations": "n/a"}), ("bad uri", {"dashboard_uri": "file:///tmp/x"})]:
    try: RaiEvidence(**{**good, **patch}); print(label, "-> accepted (BUG)")
    except ValidationError as e: print(label, "-> rejected:", e.errors()[0]["loc"][0])
