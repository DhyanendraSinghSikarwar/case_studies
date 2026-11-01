"""Q29: validate records and contract changes. Run: python3 -I q29_check.py q29_contract.yaml"""
import sys, copy, yaml
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ValidationError, create_model, Field

PYTYPE = {"string": str, "float": float, "int": int, "datetime": datetime}

def load(path):
    with open(path) as f:
        return yaml.safe_load(f)

def model_from(contract):
    """Build a pydantic model straight from the YAML so there is ONE source of truth."""
    fields = {}
    for f in contract["fields"]:
        t = PYTYPE[f["type"]]
        if "allowed" in f:
            t = Literal[tuple(f["allowed"])]
        kw = {}
        if "min" in f:
            kw["ge"] = f["min"]
        if f["nullable"]:
            fields[f["name"]] = (t | None, Field(None, **kw))
        else:
            fields[f["name"]] = (t, Field(..., **kw))
    return create_model(contract["contract"], __config__={"extra": "forbid"}, **fields)

def check_change(old, new):
    """Return a list of breaking-change reasons (empty list = compatible)."""
    problems = []
    o = {f["name"]: f for f in old["fields"]}
    n = {f["name"]: f for f in new["fields"]}
    for name, f in o.items():
        if name not in n:
            problems.append(f"removed or renamed field '{name}'")
            continue
        if n[name]["type"] != f["type"]:
            problems.append(f"type of '{name}' changed {f['type']} -> {n[name]['type']}")
        if f["nullable"] is False and n[name]["nullable"] is True:
            problems.append(f"'{name}' became nullable (consumers assumed non-null)")
        if "allowed" in f and not set(f["allowed"]) <= set(n[name].get("allowed", f["allowed"])):
            problems.append(f"'{name}' allowed values shrank")
    for name, f in n.items():
        if name not in o and f["nullable"] is False and "default" not in f:
            problems.append(f"new required field '{name}' without default")
    return problems

if __name__ == "__main__":
    c = load(sys.argv[1])
    M = model_from(c)
    good = {"txn_id": "t1", "user_id": "u1", "amount_inr": 499.0,
            "event_time": "2026-01-05T10:00:00", "channel": "UPI", "device_id": None}
    bad_records = {
        "amount in paise string": {**good, "amount_inr": "49900 paise"},
        "negative amount": {**good, "amount_inr": -5},
        "unknown channel": {**good, "channel": "WALLET"},
        "null user_id": {**good, "user_id": None},
        "extra field not in contract": {**good, "ip": "1.2.3.4"},
    }
    print("good record  ->", "PASS" if M(**good) else "?")
    for label, rec in bad_records.items():
        try:
            M(**rec); print(f"{label:28s} -> PASS (unexpected)")
        except ValidationError as e:
            errs = ", ".join(f"{'.'.join(map(str, x['loc']))}:{x['type']}" for x in e.errors())
            print(f"{label:28s} -> REJECT [{errs}]")

    additive = copy.deepcopy(c)
    additive["fields"].append({"name": "merchant_category", "type": "string", "nullable": True})
    print("\nchange A: add nullable field merchant_category ->", check_change(c, additive) or "COMPATIBLE")

    breaking = copy.deepcopy(c)
    breaking["fields"] = [f for f in breaking["fields"] if f["name"] != "amount_inr"]
    breaking["fields"].append({"name": "amount_paise", "type": "int", "nullable": False})
    print("change B: rename amount_inr -> amount_paise (int) ->")
    for p in check_change(c, breaking):
        print("   BREAKING:", p)
    sys.exit(0)
