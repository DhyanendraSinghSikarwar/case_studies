# q32_inventory.py - score exit cost per asset. Scores are OUR judgement (1 easy .. 5 hard), not measurements.
import yaml
INV = yaml.safe_load("""
assets:
  - {name: training container image,   portable: true,  kind: container,  rework: S, coupled_to: [registry auth]}
  - {name: model files (ONNX/MLflow),  portable: true,  kind: format,     rework: S, coupled_to: []}
  - {name: KFP pipeline spec,          portable: true,  kind: spec,       rework: S, coupled_to: [component images, runner]}
  - {name: Terraform modules,          portable: partly, kind: iac,       rework: L, coupled_to: [provider resources]}
  - {name: azure-ai-ml job objects,    portable: false, kind: sdk,        rework: M, coupled_to: [workspace, compute names]}
  - {name: registry metadata/lineage,  portable: false, kind: metadata,   rework: M, coupled_to: [workspace, run ids]}
  - {name: managed feature store,      portable: false, kind: managed,    rework: XL, coupled_to: [online store, offline store, SDK]}
  - {name: monitoring configs,         portable: false, kind: managed,    rework: L, coupled_to: [baseline data, alert routes]}
  - {name: IAM roles and policies,     portable: false, kind: identity,   rework: L, coupled_to: [every service]}
""")
def score(a):
    s = {"true": 1, "partly": 3, "false": 5}[str(a["portable"]).lower()]
    s += {"S": 0, "M": 1, "L": 1, "XL": 2}[a["rework"]] + (1 if len(a["coupled_to"]) >= 3 else 0)
    return min(s, 5)
rows = sorted(((score(a), a["name"], a["rework"]) for a in INV["assets"]), reverse=True)
for s, n, d in rows: print(f"exit cost {s}/5  {n:32s} rework size (our guess) {d}")
print("average:", round(sum(r[0] for r in rows) / len(rows), 2), "| portable formats lower asset cost, not the ops cost of on-call, IAM, quotas")
