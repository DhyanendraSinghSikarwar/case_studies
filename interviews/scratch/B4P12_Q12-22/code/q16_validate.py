"""Q16: validate the ownership table: every responsibility has exactly one owner, from a known set."""
import sys, copy, yaml
from collections import Counter
from pydantic import BaseModel, ValidationError, model_validator
here = sys.argv[1]
class R(BaseModel):
    name: str
    owner: str
class Table(BaseModel):
    owners: list[str]
    responsibilities: list[R]
    @model_validator(mode="after")
    def check(self):
        c = Counter(r.name for r in self.responsibilities)
        dup = [n for n, k in c.items() if k > 1]
        if dup: raise ValueError(f"responsibility listed more than once (two owners?): {dup}")
        bad = [r.name for r in self.responsibilities if r.owner not in self.owners]
        if bad: raise ValueError(f"unknown owner for: {bad}")
        need = {"identity_and_sso", "private_network_path", "quota_and_rate_limits", "request_logging_redaction",
                "provider_model_version_pin", "cost_attribution_by_team", "fallback_and_timeouts", "prompt_design",
                "retrieval_and_grounding", "answer_quality_evaluation"}
        missing = need - set(c)
        if missing: raise ValueError(f"required responsibility has no owner: {sorted(missing)}")
        return self
doc = yaml.safe_load(open(here))
t = Table(**doc)
print("good table OK:", len(t.responsibilities), "responsibilities,", dict(Counter(r.owner for r in t.responsibilities)))
for label, mut in [
    ("two owners for one item", lambda d: d["responsibilities"].append({"name": "prompt_design", "owner": "platform"})),
    ("item nobody owns", lambda d: d["responsibilities"].pop(0)),
    ("unknown owner", lambda d: d["responsibilities"][0].update(owner="vendor")),
]:
    d = copy.deepcopy(doc); mut(d)
    try: Table(**d); print(label, "-> NOT caught"); sys.exit(1)
    except ValidationError as e: print(label, "-> rejected:", e.errors()[0]["msg"].replace("Value error, ", ""))
