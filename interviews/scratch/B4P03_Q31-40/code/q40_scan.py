"""Q40: (1) scan manifests for apiVersion/kind pairs that were removed in some Kubernetes release;
(2) validate a manifest against several versions with the kubernetes-validate Python API.
The removal table holds EXAMPLES from memory of the official deprecation guide: check current docs before relying on it."""
import pathlib, sys, yaml
import kubernetes_validate

REMOVED = {   # (apiVersion, kind or '*') -> (removed in, use instead)
 ("extensions/v1beta1", "Ingress"):          ("1.22", "networking.k8s.io/v1"),
 ("networking.k8s.io/v1beta1", "Ingress"):   ("1.22", "networking.k8s.io/v1"),
 ("batch/v1beta1", "CronJob"):               ("1.25", "batch/v1"),
 ("autoscaling/v2beta1", "HorizontalPodAutoscaler"): ("1.25", "autoscaling/v2"),
 ("autoscaling/v2beta2", "HorizontalPodAutoscaler"): ("1.26", "autoscaling/v2"),
 ("policy/v1beta1", "PodDisruptionBudget"):  ("1.25", "policy/v1"),
 ("policy/v1beta1", "PodSecurityPolicy"):    ("1.25", "(no replacement object: use Pod Security Admission)"),
 ("flowcontrol.apiserver.k8s.io/v1beta2", "*"): ("1.29", "flowcontrol.apiserver.k8s.io/v1"),
}

def scan(path):
    hits = []
    for d in yaml.safe_load_all(path.read_text()):
        if not isinstance(d, dict): continue
        key = (d.get("apiVersion"), d.get("kind"))
        hit = REMOVED.get(key) or REMOVED.get((key[0], "*"))
        if hit: hits.append((d["kind"], d["metadata"]["name"], key[0], *hit))
    return hits

root = pathlib.Path(__file__).resolve().parent / "q40_manifests"
print("== removed-API scan")
found = 0
for f in sorted(root.glob("*.yaml")):
    for kind, name, api, rem, use in scan(f):
        found += 1; print(f"{f.name}: {kind}/{name} uses {api}, removed in {rem}, use {use}")
print(f"{found} problem(s)")

print("\n== kubernetes-validate (strict) per version")
for f in ("ok_deploy.yaml", "old_hpa_cronjob.yaml", "old_ingress.yaml"):
    docs = [d for d in yaml.safe_load_all((root / f).read_text())]
    for ver in ("1.25", "1.26", "1.37"):
        for d in docs:
            try:
                kubernetes_validate.validate(d, ver, strict=True)
                r = "ok"
            except kubernetes_validate.SchemaNotFoundError:
                r = "no schema in that release (API removed or unknown)"
            except kubernetes_validate.ValidationError as e:
                r = "INVALID: " + str(e).splitlines()[0][:70]
            except Exception as e:
                r = type(e).__name__
            print(f"{f:22} {d['kind']:24} v{ver:5} {r}")
