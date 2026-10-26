# q31.py - validate the launch checklist with pyyaml. No model endpoint is called.
import sys, yaml
d = yaml.safe_load(open(sys.argv[1]))
REQUIRED_IDS = {"identity", "network", "quota_region", "model_version", "eval_gate", "logging", "cost_attribution", "fallback"}
errs = []
for k in ("service", "provider", "owner", "mlops_owns", "book2_owns"):
    if k not in d: errs.append(f"missing top-level key {k}")
if d.get("provider") not in ("azure_openai", "gemini_on_vertex"): errs.append("provider must be azure_openai or gemini_on_vertex")
ids = [i.get("id") for i in d["mlops_owns"]]
if len(ids) != len(set(ids)): errs.append("duplicate ids")
for miss in sorted(REQUIRED_IDS - set(ids)): errs.append(f"missing item {miss}")
for i in d["mlops_owns"]:
    for f in ("id", "check", "evidence"):
        if not i.get(f): errs.append(f"{i.get('id')}: empty {f}")
overlap = set(d["book2_owns"]) & set(ids)
if overlap: errs.append(f"items in both lists: {overlap}")
print("items:", len(ids), "| book2 topics:", d["book2_owns"])
print("called_real_endpoint:", d["called_real_endpoint"])
print("RESULT:", "OK" if not errs else errs)
# negative test
d["mlops_owns"] = [i for i in d["mlops_owns"] if i["id"] != "model_version"]
ids = {i["id"] for i in d["mlops_owns"]}
print("negative test (drop model_version) ->", sorted(REQUIRED_IDS - ids))
