# q35.py - minimal common model-metadata record for a cross-cloud catalogue; validate sample records with pydantic + pyyaml.
import yaml, pydantic
from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator
print("pydantic", pydantic.VERSION)
class Lineage(BaseModel):
    training_data: list[str] = Field(min_length=1)      # asset refs (azureml:name:ver / bq or gs URI)
    code_commit: str = Field(pattern=r"^[0-9a-f]{7,40}$")
    pipeline_run: Optional[str] = None
class ModelRecord(BaseModel):
    model_id: str                                       # OUR id, same across clouds
    version: int = Field(ge=1)
    cloud: Literal["azure", "gcp"]
    platform_ref: str                                   # the cloud's own handle
    owner: str = Field(pattern=r"^[^@\s]+@[^@\s]+$")
    approver: Optional[str] = None
    stage: Literal["dev", "staging", "prod"]
    risk_tier: Literal["low", "medium", "high"]
    model_card_url: Optional[str] = None
    lineage: Lineage
    @model_validator(mode="after")
    def rules(self):
        prefix = {"azure": "azureml:", "gcp": "projects/"}[self.cloud]
        if not self.platform_ref.startswith(prefix): raise ValueError(f"platform_ref must start with {prefix!r} for {self.cloud}")
        if self.stage == "prod":
            if not self.approver: raise ValueError("prod needs an approver")
            if self.approver == self.owner: raise ValueError("approver must differ from owner")
            if not self.model_card_url: raise ValueError("prod needs a model card")
        return self
RECORDS = yaml.safe_load("""
- {model_id: churn, version: 7, cloud: azure, platform_ref: "azureml:churn:7", owner: asha@corp.example, approver: ravi@corp.example,
   stage: prod, risk_tier: medium, model_card_url: "https://wiki.example/cards/churn-7",
   lineage: {training_data: ["azureml:churn-data:12"], code_commit: 3fa91bc, pipeline_run: "run-001"}}
- {model_id: fraud, version: 3, cloud: gcp, platform_ref: "projects/p/locations/asia-south1/models/123", owner: dev@corp.example,
   approver: meera@corp.example, stage: prod, risk_tier: high, model_card_url: "https://wiki.example/cards/fraud-3",
   lineage: {training_data: ["bq://p.ds.txns_v5"], code_commit: 9d0c2e4a}}
- {model_id: churn, version: 8, cloud: azure, platform_ref: "azureml:churn:8", owner: asha@corp.example, approver: asha@corp.example,
   stage: prod, risk_tier: medium, model_card_url: "https://wiki.example/cards/churn-8",
   lineage: {training_data: ["azureml:churn-data:13"], code_commit: 77aa12f}}
- {model_id: rec, version: 1, cloud: gcp, platform_ref: "azureml:rec:1", owner: dev@corp.example,
   stage: prod, risk_tier: low, lineage: {training_data: [], code_commit: "xyz"}}
""")
for r in RECORDS:
    try:
        ModelRecord(**r); print(f"OK   {r['model_id']} v{r['version']} ({r['cloud']})")
    except pydantic.ValidationError as e:
        msgs = sorted({f"{'.'.join(map(str, x['loc'])) or 'record'}: {x['msg'].replace('Value error, ', '')}" for x in e.errors()})
        print(f"FAIL {r['model_id']} v{r['version']} ({r['cloud']})"); [print("     -", m) for m in msgs]
