# Q32: policy as code. pydantic checks shape and types; plain Python checks the rules; all violations are returned.
import re, yaml, pathlib, datetime
from pydantic import BaseModel, ValidationError
from typing import Optional
TODAY = datetime.date(2026, 10, 26)                   # fixed so the output is repeatable
POL = yaml.safe_load(pathlib.Path("q32_policy.yaml").read_text())
class Manifest(BaseModel):
    name: str
    image: str
    region: str
    gpus: int = 0
    public_endpoint: bool = False
    tags: dict[str, str] = {}
def rules(m: Manifest):
    v = []
    for t in POL["required_tags"]:
        if t not in m.tags: v.append(("required_tag", f"missing tag {t}"))
    dc = m.tags.get("data_classification")
    if dc and dc not in POL["data_classifications"]: v.append(("required_tag", f"bad data_classification {dc}"))
    if m.region not in POL["allowed_regions"]: v.append(("allowed_region", f"region {m.region} not allowed"))
    if not any(m.image.startswith(r) for r in POL["approved_registries"]): v.append(("registry", f"image {m.image.split('@')[0]} not from an approved registry"))
    if POL["require_digest"] and not re.search(r"@sha256:[0-9a-f]{64}$", m.image): v.append(("digest", "image not pinned by digest"))
    if POL["restricted_no_public_endpoint"] and dc == "restricted" and m.public_endpoint: v.append(("public_endpoint", "restricted data behind a public endpoint"))
    if m.gpus > POL["max_gpus_without_approval"]: v.append(("max_gpus", f"{m.gpus} GPUs > {POL['max_gpus_without_approval']}"))
    return v
def apply_exceptions(name, vs):
    out = []
    for rule, msg in vs:
        ex = [e for e in POL["exceptions"] if e["rule"] == rule and e["manifest"] == name]
        if ex and datetime.date.fromisoformat(ex[0]["expires"]) >= TODAY: out.append((rule, msg + f"  [waived by {ex[0]['approved_by']} until {ex[0]['expires']}]", True))
        elif ex: out.append((rule, msg + f"  [exception EXPIRED {ex[0]['expires']}]", False))
        else: out.append((rule, msg, False))
    return out
D = "@sha256:" + "a" * 64; REG = "registry.internal.example/ml/"
MANIFESTS = [
 {"name": "fraud-api", "image": REG + "fraud" + D, "region": "in-west", "gpus": 0, "tags": {"owner": "risk-ml", "cost_center": "cc42", "data_classification": "restricted", "env": "prod"}},
 {"name": "scratch-notebook", "image": "docker.io/library/python:latest", "region": "us-1", "gpus": 1, "public_endpoint": True, "tags": {"owner": "ds-7"}},
 {"name": "big-train-job", "image": REG + "train" + D, "region": "in-south", "gpus": 16, "tags": {"owner": "ds-2", "cost_center": "cc9", "data_classification": "internal", "env": "dev"}},
 {"name": "eu-pilot", "image": REG + "pilot" + D, "region": "eu-1", "gpus": 2, "tags": {"owner": "ds-3", "cost_center": "cc9", "data_classification": "public", "env": "dev"}},
 {"name": "leaky-scorer", "image": REG + "score:v3", "region": "in-west", "gpus": 1, "public_endpoint": True, "tags": {"owner": "ds-4", "cost_center": "cc1", "data_classification": "restricted", "env": "prod"}},
 {"name": "bad-types", "image": REG + "x" + D, "region": "in-west", "gpus": "many", "tags": {}},
]
for raw in MANIFESTS:
    try: m = Manifest(**raw)
    except ValidationError as e:
        print(f"{raw['name']:<17} REJECT (schema)"); [print("    -", er["loc"], er["msg"]) for er in e.errors()]; continue
    res = apply_exceptions(m.name, rules(m)); blocking = [r for r in res if not r[2]]
    print(f"{m.name:<17}", "ALLOW" if not blocking else f"REJECT ({len(blocking)} violations)", "" if not res or blocking else f"(with {len(res)} waived)")
    for rule, msg, waived in res: print("   ", "waived" if waived else "  FAIL", rule, "-", msg)
