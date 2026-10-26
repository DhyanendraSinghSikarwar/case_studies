"""Q32: checks a portfolio project folder for the things a K8s-for-ML repo should show. Runs on a temp demo repo."""
import pathlib, tempfile, yaml

def check(root):
    root = pathlib.Path(root)
    docs = []
    for p in list(root.rglob("*.yaml")) + list(root.rglob("*.yml")):
        if "templates" in p.parts:   # Helm templates hold {{ }} and are not plain YAML
            docs.append(("tmpl", p.read_text()))
            continue
        try:
            for d in yaml.safe_load_all(p.read_text()):
                if isinstance(d, dict): docs.append(("yaml", d))
        except yaml.YAMLError:
            pass
    text = " ".join(str(d) for _, d in docs)
    return {
      "Chart.yaml (Helm chart)": (root / "chart" / "Chart.yaml").exists(),
      "values.yaml":              (root / "chart" / "values.yaml").exists(),
      "HPA":                      "HorizontalPodAutoscaler" in text,
      "readiness probe":          "readinessProbe" in text,
      "startup probe":            "startupProbe" in text,
      "canary (2nd Deployment or weight)": "canary" in text.lower(),
      "resource requests/limits": "requests" in text and "limits" in text,
      "README with run steps":    (root / "README.md").exists(),
    }

with tempfile.TemporaryDirectory() as t:
    r = pathlib.Path(t)
    (r / "chart" / "templates").mkdir(parents=True)
    (r / "chart" / "Chart.yaml").write_text("apiVersion: v2\nname: model-api\nversion: 0.1.0\n")
    (r / "chart" / "values.yaml").write_text("replicas: 2\n")
    (r / "chart" / "templates" / "deploy.yaml").write_text("kind: Deployment\n# {{ .Values.replicas }} readinessProbe canary\n")
    (r / "k8s").mkdir()
    (r / "k8s" / "hpa.yaml").write_text("apiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nmetadata: {name: model-api}\n")
    (r / "k8s" / "deploy.yaml").write_text(
        "apiVersion: apps/v1\nkind: Deployment\nmetadata: {name: model-api}\nspec:\n  template:\n    spec:\n      containers:\n"
        "      - name: api\n        readinessProbe: {httpGet: {path: /ready, port: 8000}}\n"
        "        resources: {requests: {cpu: 100m}, limits: {memory: 256Mi}}\n")
    for k, v in check(r).items():
        print(f"{'PASS' if v else 'MISSING':8}{k}")
