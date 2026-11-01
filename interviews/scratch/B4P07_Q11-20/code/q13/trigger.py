"""Decide whether a retrain should start. Pure function plus a tiny CLI."""
import argparse, json, datetime as dt

MIN_NEW_ROWS = 5000
COOLDOWN_H = 24
MAX_RUNS_PER_WEEK = 3


def decide(event, new_rows, last_train, now, runs_last_7d, drift_alert=False):
    """Return (go, reason). last_train and now are datetimes."""
    if runs_last_7d >= MAX_RUNS_PER_WEEK:
        return False, "cost cap: weekly retrain budget used"
    if event == "workflow_dispatch":                      # a human decided, only the cost cap applies
        return True, "manual request"
    age_h = (now - last_train).total_seconds() / 3600 if last_train else None
    if age_h is not None and age_h < COOLDOWN_H:
        return False, f"cooldown: last train {age_h:.0f}h ago, need {COOLDOWN_H}h"
    if event == "repository_dispatch":
        if not drift_alert:
            return False, "dispatch without drift flag"
        if new_rows < MIN_NEW_ROWS:
            return False, f"only {new_rows} new rows, need {MIN_NEW_ROWS}"
        return True, "drift alert with enough fresh data"
    if event == "schedule":
        if new_rows < MIN_NEW_ROWS:
            return False, f"only {new_rows} new rows, need {MIN_NEW_ROWS}"
        return True, "scheduled run with enough fresh data"
    return False, f"event {event} does not retrain"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--event", required=True)
    p.add_argument("--state", required=True)
    a = p.parse_args()
    s = json.load(open(a.state))
    now = dt.datetime.fromisoformat(s.get("now", dt.datetime.now(dt.timezone.utc).isoformat()))
    last = dt.datetime.fromisoformat(s["last_train"]) if s.get("last_train") else None
    go, why = decide(a.event, s["new_rows"], last, now, s["runs_last_7d"], s.get("drift_alert", False))
    print(f"go={'true' if go else 'false'}")
    print(f"why={why}")
