# Q26: validate a W&B sweep config offline (pyyaml only; no wandb import, no network).
import sys, yaml
METHODS = {"grid", "random", "bayes"}
DISTS_RANGE = {"uniform", "int_uniform", "log_uniform_values", "q_uniform", "q_log_uniform_values"}
def check(cfg, logged_metrics):
    errs = []
    if cfg.get("method") not in METHODS: errs.append(f"method must be one of {sorted(METHODS)}, got {cfg.get('method')!r}")
    m = cfg.get("metric", {})
    if cfg.get("method") == "bayes" and not m: errs.append("bayes needs a metric block")
    if m and m.get("goal") not in {"minimize", "maximize"}: errs.append(f"metric.goal invalid: {m.get('goal')!r}")
    if m and m.get("name") not in logged_metrics: errs.append(f"metric.name {m.get('name')!r} is never logged by train.py (known: {sorted(logged_metrics)})")
    params = cfg.get("parameters") or {}
    if not params: errs.append("no parameters")
    for k, p in params.items():
        if "values" in p:
            if not p["values"]: errs.append(f"{k}: empty values")
        elif "value" in p: pass
        else:
            d = p.get("distribution", "uniform")
            if d in DISTS_RANGE:
                lo, hi = p.get("min"), p.get("max")
                if lo is None or hi is None: errs.append(f"{k}: {d} needs min and max")
                elif lo >= hi: errs.append(f"{k}: min {lo} must be < max {hi}")
                elif d.startswith(("log", "q_log")) and lo <= 0: errs.append(f"{k}: log distribution needs min > 0")
            else: errs.append(f"{k}: unknown distribution {d!r}")
        if cfg.get("method") == "grid" and "values" not in p and "value" not in p:
            errs.append(f"{k}: grid search needs discrete values, not a range")
    if "early_terminate" in cfg and cfg["early_terminate"].get("type") != "hyperband":
        errs.append("early_terminate.type should be hyperband")
    return errs

cfg = yaml.safe_load(open("sweep.yaml"))
logged = {"val_auc", "val_loss", "train_loss"}
print("good config  ->", check(cfg, logged) or "OK")
bad = yaml.safe_load(open("sweep.yaml"))
bad["method"] = "grid"; bad["metric"]["name"] = "val_acc"
bad["parameters"]["lr"]["min"] = 0.5
bad["parameters"]["dropout"]["distribution"] = "normalish"
print("broken config ->")
for e in check(bad, logged): print("   -", e)
print("grid blow-up check: 5 lr values * 5 dropout values * 3 batch sizes * 2 optimizers =", 5*5*3*2, "runs")
