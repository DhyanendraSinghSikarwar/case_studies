# Structure check with pyyaml only. No cluster, no CRD, so this does NOT prove KServe would accept the file.
import sys, yaml
d = yaml.safe_load(open(sys.argv[1])); errs = []
def need(cond, msg):
    if not cond: errs.append(msg)
need(d.get("apiVersion", "").startswith("serving.kserve.io/"), "apiVersion should be serving.kserve.io/...")
need(d.get("kind") == "InferenceService", "kind must be InferenceService")
need(d.get("metadata", {}).get("name"), "metadata.name missing")
p = d.get("spec", {}).get("predictor", {})
need(p, "spec.predictor missing")
m = p.get("model", {})
need(m.get("modelFormat", {}).get("name"), "predictor.model.modelFormat.name missing")
need(str(m.get("storageUri", "")).split("://")[0] in ("s3", "gs", "pvc", "https", "hf", "oci"), "storageUri scheme unexpected")
need(0 <= p.get("canaryTrafficPercent", 0) <= 100, "canaryTrafficPercent must be 0..100")
need(p.get("minReplicas", 0) <= p.get("maxReplicas", 10**9), "minReplicas > maxReplicas")
print("structure problems:", errs or "none")
d["spec"]["predictor"]["canaryTrafficPercent"] = 150; d["kind"] = "InferenceServce"
errs.clear()
need(d["kind"] == "InferenceService", "kind must be InferenceService"); need(0 <= d["spec"]["predictor"]["canaryTrafficPercent"] <= 100, "canaryTrafficPercent must be 0..100")
print("after two deliberate typos:", errs)
