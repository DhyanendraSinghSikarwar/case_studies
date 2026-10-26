"""Semantic checks for Job/CronJob manifests + next-N cron run times. Pure Python, no cluster."""
import sys, yaml
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]   # min hour dom month dow (0 = Sunday)

def parse_field(text, lo, hi):
    out = set()
    for part in text.split(","):
        step = 1
        if "/" in part:
            part, s = part.split("/"); step = int(s)
        if part == "*": a, b = lo, hi
        elif "-" in part: a, b = map(int, part.split("-"))
        else: a = int(part); b = hi if step > 1 else a
        out.update(range(a, b + 1, step))
    assert all(lo <= v <= hi for v in out), f"out of range in {text!r}"
    return out

def next_runs(schedule, start, n=5):
    f = schedule.split()
    assert len(f) == 5, "need 5 fields"
    mins, hrs, doms, mons, dows = (parse_field(x, *r) for x, r in zip(f, RANGES))
    dom_star, dow_star = f[2] == "*", f[4] == "*"
    t = start.replace(second=0, microsecond=0) + timedelta(minutes=1)
    runs = []
    while len(runs) < n:
        dow = (t.weekday() + 1) % 7                      # Python Monday=0 -> cron Sunday=0
        if dom_star or dow_star: day_ok = t.day in doms and dow in dows
        else: day_ok = t.day in doms or dow in dows      # both restricted: cron uses OR
        if t.minute in mins and t.hour in hrs and t.month in mons and day_ok:
            runs.append(t)
        t += timedelta(minutes=1)
    return runs

def check_pod_spec(spec, where, problems):
    if spec.get("restartPolicy") not in ("Never", "OnFailure"):
        problems.append(f"{where}: restartPolicy must be Never or OnFailure for batch pods")
    for c in spec["containers"]:
        r = c.get("resources", {})
        if "memory" not in r.get("limits", {}):
            problems.append(f"{where}: container {c['name']} has no memory limit")

def check(doc):
    problems = []
    kind, name = doc["kind"], doc["metadata"]["name"]
    job = doc["spec"]["jobTemplate"]["spec"] if kind == "CronJob" else doc["spec"]
    for f in ("backoffLimit", "activeDeadlineSeconds", "ttlSecondsAfterFinished"):
        if f not in job: problems.append(f"{kind}/{name}: {f} not set")
    check_pod_spec(job["template"]["spec"], f"{kind}/{name}", problems)
    if kind == "CronJob":
        if doc["spec"].get("concurrencyPolicy", "Allow") == "Allow":
            problems.append(f"CronJob/{name}: concurrencyPolicy Allow lets runs overlap")
        if "timeZone" not in doc["spec"]:
            problems.append(f"CronJob/{name}: no timeZone")
    return problems

if __name__ == "__main__":
    for path in sys.argv[1:]:
        for doc in yaml.safe_load_all(open(path)):
            probs = check(doc)
            print(f"{doc['kind']}/{doc['metadata']['name']}: {'OK' if not probs else probs}")
            if doc["kind"] == "CronJob":
                tz = ZoneInfo(doc["spec"].get("timeZone", "UTC"))
                now = datetime(2026, 10, 26, 22, 10, tzinfo=tz)      # fixed 'now' so output is repeatable
                print(f"  schedule {doc['spec']['schedule']!r} in {tz.key}, after {now:%Y-%m-%d %H:%M}:")
                for t in next_runs(doc["spec"]["schedule"], now):
                    print(f"    {t:%a %Y-%m-%d %H:%M %Z}  =  {t.astimezone(timezone.utc):%H:%M} UTC")
    # edge cases worth knowing
    t0 = datetime(2026, 10, 26, 0, 0, tzinfo=timezone.utc)
    print("every 15 min :", [f"{t:%H:%M}" for t in next_runs("*/15 * * * *", t0, 4)])
    print("'0 9 13 * 5' :", [f"{t:%a %m-%d}" for t in next_runs("0 9 13 * 5", t0, 4)], "(13th OR any Friday)")
