# Q30: validate invented data flows against policy-as-data. Plain Python + pyyaml. Not legal advice.
import yaml, pathlib
P = yaml.safe_load(pathlib.Path("q30_policy.yaml").read_text())
IN = {r for r, v in P["regions"].items() if v["country"] == "IN"}
def check(f):
    v = []
    for r in (f["from"], f["to"]):
        if r not in P["regions"]: v.append(f"unknown region {r}")
    unknown = [x for x in f["fields"] if x not in P["fields"]]
    if unknown: v.append(f"unclassified fields {unknown} (default deny)")
    restricted = [x for x in f["fields"] if P["fields"].get(x) == "restricted"]
    if f["to"] in P["regions"] and f["to"] not in IN and restricted:
        ok = P["rules"]["allow_tokenised_abroad"] and f.get("transform") == "tokenised" and f.get("vault_region") in IN
        if not ok: v.append(f"restricted {restricted} to non-India region {f['to']} (transform={f.get('transform')})")
    if f.get("kind") == "store" and restricted and f.get("key_region") not in IN:
        v.append(f"restricted store with key in {f.get('key_region')}, rule wants country {P['rules']['keys_must_be_in_country']}")
    if f.get("kind") == "log" and f["to"] not in IN:
        bad = [x for x in f["fields"] if P["fields"].get(x) not in P["rules"]["logs_may_leave"]]
        if bad: v.append(f"log leaving India carries {bad}")
    return v
FLOWS = [
 {"name": "train-data-in-india",        "from": "in-west", "to": "in-south", "fields": ["pan_number", "txn_amount"], "kind": "store", "key_region": "in-west"},
 {"name": "raw-pan-to-global-ml",       "from": "in-west", "to": "us-1", "fields": ["pan_number", "txn_amount"], "transform": "none"},
 {"name": "tokenised-to-global-ml",     "from": "in-west", "to": "us-1", "fields": ["txn_amount", "merchant_cat"], "transform": "tokenised", "vault_region": "in-west"},
 {"name": "tokenised-vault-abroad",     "from": "in-west", "to": "eu-1", "fields": ["phone"], "transform": "tokenised", "vault_region": "eu-1"},
 {"name": "logs-with-name",             "from": "in-south", "to": "us-1", "fields": ["customer_name", "device_hash"], "kind": "log"},
 {"name": "store-key-abroad",           "from": "in-west", "to": "in-south", "fields": ["account_number"], "kind": "store", "key_region": "us-1"},
 {"name": "new-field-nobody-classified","from": "in-west", "to": "in-south", "fields": ["salary_band"]},
]
for f in FLOWS:
    v = check(f); print(f"{f['name']:<30}", "ALLOW" if not v else "REJECT")
    for x in v: print("    -", x)
