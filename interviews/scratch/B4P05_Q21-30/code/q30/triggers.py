"""Retraining trigger decision. Pure Python; the inputs come from your monitoring job (Part 8 owns drift detection)."""
from datetime import date


def decide(today, last_trained, new_rows, drift_psi, live_auc, *,
           max_age_days=30, min_new_rows=100_000, psi_limit=0.25, auc_floor=0.80):
    """Return (should_train, reason). First matching rule wins, ordered from most to least urgent."""
    if live_auc is not None and live_auc < auc_floor:
        return True, f"performance: live AUC {live_auc} < floor {auc_floor}"
    if drift_psi is not None and drift_psi > psi_limit:
        return True, f"drift: PSI {drift_psi} > {psi_limit}"
    if new_rows >= min_new_rows:
        return True, f"volume: {new_rows} new rows >= {min_new_rows}"
    age = (today - last_trained).days
    if age >= max_age_days:
        return True, f"schedule: model is {age} days old (limit {max_age_days})"
    return False, f"no trigger: age {age}d, rows {new_rows}, psi {drift_psi}, auc {live_auc}"


def build_conf(today, reason, *, dry_run=False, model_version="auto", lookback_days=30):
    """The parameters a triggered run takes. Same shape for Airflow conf, Prefect parameters and KFP arguments."""
    return {"reason": reason, "data_end": today.isoformat(), "lookback_days": lookback_days,
            "model_version": model_version, "dry_run": dry_run}


if __name__ == "__main__":
    today, last = date(2026, 10, 26), date(2026, 10, 1)
    cases = [
        ("quiet", dict(new_rows=5_000, drift_psi=0.05, live_auc=0.86)),
        ("volume", dict(new_rows=250_000, drift_psi=0.05, live_auc=0.86)),
        ("drift", dict(new_rows=5_000, drift_psi=0.31, live_auc=0.86)),
        ("perf+drift", dict(new_rows=5_000, drift_psi=0.31, live_auc=0.74)),
        ("no labels yet", dict(new_rows=5_000, drift_psi=0.05, live_auc=None)),
    ]
    for name, kw in cases:
        print(f"{name:14}", decide(today, last, **kw))
    print("old model     ", decide(today, date(2026, 9, 1), 5_000, 0.05, 0.86))
    print(build_conf(today, "drift: PSI 0.31 > 0.25", dry_run=True))
