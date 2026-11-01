"""Validate required InferenceService fields (our own short list, not the real CRD schema)
and compute the canary traffic split. Run on the manifest and on deliberately broken variants."""
import copy, yaml

def get(d, path):
    for p in path.split("."):
        if not isinstance(d, dict) or p not in d: return None
        d = d[p]
    return d

REQUIRED = ["apiVersion", "kind", "metadata.name", "spec.predictor.model.modelFormat.name", "spec.predictor.model.storageUri"]

def check(doc):
    errs = [f"missing {p}" for p in REQUIRED if get(doc, p) is None]
    if doc.get("kind") != "InferenceService": errs.append("kind is not InferenceService")
    pred = get(doc, "spec.predictor") or {}
    c = pred.get("canaryTrafficPercent")
    if c is not None and not (0 <= c <= 100): errs.append(f"canaryTrafficPercent {c} not in 0..100")
    lo = pred.get("minReplicas", 1)
    hi = pred.get("maxReplicas", lo)
    if hi < lo: errs.append(f"maxReplicas {hi} < minReplicas {lo}")
    uri = get(doc, "spec.predictor.model.storageUri") or ""
    if uri and uri.rstrip("/").endswith("latest"): errs.append("storageUri uses 'latest': not reproducible")
    return errs

def split(doc):
    c = get(doc, "spec.predictor.canaryTrafficPercent")
    if c is None: return {"latest revision": 100}
    if not 0 <= c <= 100: return "invalid"
    return {"latest revision (new)": c, "previous rolled-out revision": 100 - c}

good = yaml.safe_load(open("isvc.yaml"))
print("good manifest errors:", check(good) or "none", "| traffic:", split(good))

def variant(name, edit):
    d = copy.deepcopy(good); edit(d); print(f"{name}: {check(d) or 'none'} | traffic: {split(d)}")

variant("no storageUri", lambda d: d["spec"]["predictor"]["model"].pop("storageUri"))
variant("canary 150", lambda d: d["spec"]["predictor"].update(canaryTrafficPercent=150))
variant("canary 0 (new revision gets nothing)", lambda d: d["spec"]["predictor"].update(canaryTrafficPercent=0))
variant("promote: remove canaryTrafficPercent", lambda d: d["spec"]["predictor"].pop("canaryTrafficPercent"))
variant("max < min", lambda d: d["spec"]["predictor"].update(minReplicas=3, maxReplicas=2))
variant("latest model", lambda d: d["spec"]["predictor"]["model"].update(storageUri="s3://m/fraud/latest"))
