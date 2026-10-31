import yaml
from pydantic import BaseModel, field_validator
from typing import List
DOC = """
model: retail_credit_score_v1
requirements:
  - {id: R1, area: approval, control: "Model risk committee approves before go-live", owner: model_risk, evidence: approval_minutes}
  - {id: R2, area: explainability, control: "Top reasons per decline stored with each decision", owner: ml_team, evidence: reason_code_log}
  - {id: R3, area: fairness, control: "Fairness review across agreed groups before approval", owner: model_risk, evidence: fairness_report}
  - {id: R4, area: audit, control: "Decision log kept for retention period set by bank policy", owner: compliance, evidence: log_retention_policy}
  - {id: R5, area: residency, control: "Customer data processed only in approved locations (check RBI site and bank policy)", owner: security, evidence: architecture_review}
  - {id: R6, area: outsourcing, control: "Cloud and third-party use follows bank outsourcing policy (check current rules)", owner: vendor_risk, evidence: vendor_assessment}
  - {id: R7, area: validation, control: "Independent team validates, not the builders", owner: validation_team, evidence: validation_report}
"""
AREAS={"approval","explainability","fairness","audit","residency","outsourcing","validation"}
class Req(BaseModel):
    id:str; area:str; control:str; owner:str; evidence:str
    @field_validator("area")
    @classmethod
    def ok(cls,v):
        if v not in AREAS: raise ValueError("unknown area "+v)
        return v
class Doc(BaseModel):
    model:str; requirements:List[Req]
    @field_validator("requirements")
    @classmethod
    def cover(cls,v):
        miss=AREAS-{r.area for r in v}
        if miss: raise ValueError(f"missing areas {sorted(miss)}")
        return v
d=Doc(**yaml.safe_load(DOC))
print("valid; requirements:",len(d.requirements))
for r in d.requirements: print(r.id,r.area,"->",r.owner,"/",r.evidence)
bad=yaml.safe_load(DOC); bad["requirements"]=bad["requirements"][:-1]
try: Doc(**bad)
except Exception as e: print("rejected incomplete doc:", e.errors()[0]["msg"])
