"""(1) base64 is not encryption, (2) hash of ConfigMap data -> pod-template annotation -> rollout trigger."""
import base64, hashlib, json, sys, yaml

docs = {d["kind"]: d for d in yaml.safe_load_all(open(sys.argv[1]))}

for k, v in docs["Secret"]["data"].items():
    print(f"{k}: stored as {v!r} -> decoded {base64.b64decode(v).decode()!r}   (anyone with get-secret RBAC can do this)")

def config_hash(cm):
    return hashlib.sha256(json.dumps(cm["data"], sort_keys=True).encode()).hexdigest()[:16]

cm = docs["ConfigMap"]
h1 = config_hash(cm)
cm["data"]["THRESHOLD"] = "0.70"                  # someone edits the threshold
h2 = config_hash(cm)
print("config hash before:", h1)
print("config hash after :", h2, "->", "template changes, Deployment rolls" if h1 != h2 else "no change")
print("same data, other key order:", config_hash({"data": dict(reversed(list(cm["data"].items())))}) == h2)

dep = docs["Deployment"]
dep["spec"]["template"]["metadata"]["annotations"]["checksum/config"] = h2
print("annotation now:", dep["spec"]["template"]["metadata"]["annotations"])
yaml.safe_dump_all(docs.values(), open("config.rendered.yaml", "w"), sort_keys=False)
