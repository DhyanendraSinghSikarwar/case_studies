from dataclasses import dataclass
import numpy as np

@dataclass
class Day:
    d: int; drift: float; acc: float | None; dq_ok: bool; new_rows: int

COOLDOWN, MAX_AGE, MIN_ROWS, DRIFT_HI, ACC_FLOOR = 7, 30, 20000, 0.2, 0.75

def decide(day, hist, last_train, high_risk=True):
    since = day.d - last_train
    drift_run = len(hist) >= 3 and all(h.drift > DRIFT_HI for h in hist[-3:])   # 3 days in a row
    reason = None
    if day.acc is not None and day.acc < ACC_FLOOR: reason = f"performance {day.acc:.2f} < {ACC_FLOOR}"
    elif drift_run:                                 reason = "drift above limit 3 days running"
    elif since >= MAX_AGE:                          reason = f"scheduled: model is {since}d old"
    if reason is None:                     return "none"
    if not day.dq_ok:                      return f"VETO ({reason}): data-quality gate failed"
    if since < COOLDOWN:                   return f"hold: cooldown ({since}d < {COOLDOWN}d)"
    if day.new_rows < MIN_ROWS:            return "hold: not enough new rows"
    return ("RETRAIN needs human approval: " if high_risk else "RETRAIN: ") + reason

rng = np.random.default_rng(30)
WORLD_CHANGE = 12          # the world shifts on day 12; a retrain after that fixes drift and, later, accuracy
last_train, hist, rows_since = 0, [], 0
print(f"{'day':>3} {'drift':>6} {'acc':>6} {'dq':>3} {'rows':>6}  decision")
for d in range(1, 51):
    rows_since += int(rng.integers(4000, 9000))
    stale = d >= WORLD_CHANGE and last_train < WORLD_CHANGE          # model still trained on the old world
    drift = 0.08 + rng.normal(0, 0.02) + (0.18 if stale else 0)
    acc = None if d < 8 else round(0.82 - (0.09 if stale and d >= 14 else 0) + rng.normal(0, 0.01), 3)
    day = Day(d, round(drift, 3), acc, dq_ok=not (13 <= d <= 14), new_rows=rows_since)
    hist.append(day)
    out = decide(day, hist, last_train)
    if out.startswith("RETRAIN"):          # assume the approval comes and training finishes the same day
        last_train, rows_since = d, 0
    if out != "none" and not out.startswith("hold: cooldown"):
        print(f"{d:>3} {day.drift:6.3f} {str(day.acc):>6} {'ok' if day.dq_ok else 'BAD':>3} {day.new_rows:>6}  {out}")
print("last training day:", last_train, "| days 1-50 with 'none' or cooldown holds are not printed")
