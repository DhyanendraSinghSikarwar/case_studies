"""Compare output folders of the old cron job and the new orchestrated job. Flags: missing/extra files, row-count and key diffs, value diffs beyond tolerance."""
import csv, os, sys, tempfile

IGNORE = {"generated_at"}            # columns that legitimately differ between runs
TOL = 1e-6

def load(path, key):
    with open(path, newline="") as f:
        return {r[key]: {k: v for k, v in r.items() if k not in IGNORE} for r in csv.DictReader(f)}

def same(a, b):
    try: return abs(float(a) - float(b)) <= TOL
    except ValueError: return a == b

def compare_dirs(old, new, key="id"):
    findings = []
    fo, fn = set(os.listdir(old)), set(os.listdir(new))
    findings += [f"MISSING in new: {f}" for f in sorted(fo - fn)] + [f"EXTRA in new: {f}" for f in sorted(fn - fo)]
    for f in sorted(fo & fn):
        o, n = load(os.path.join(old, f), key), load(os.path.join(new, f), key)
        if len(o) != len(n): findings.append(f"{f}: row count old={len(o)} new={len(n)}")
        for k in sorted(set(o) - set(n)): findings.append(f"{f}: key {k} only in old")
        for k in sorted(set(n) - set(o)): findings.append(f"{f}: key {k} only in new")
        for k in sorted(set(o) & set(n)):
            for col, v in o[k].items():
                if not same(v, n[k].get(col, "<absent>")):
                    findings.append(f"{f}: key {k} col {col} old={v} new={n[k].get(col)}")
    return findings

def write(d, name, header, rows):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        res = compare_dirs(sys.argv[1], sys.argv[2])
    else:                                         # demo data
        t = tempfile.mkdtemp(); o, n = os.path.join(t, "old"), os.path.join(t, "new")
        h = ["id", "score", "generated_at"]
        write(o, "scores.csv", h, [(1, 0.50, "09:00"), (2, 0.70, "09:00"), (3, 0.90, "09:00")])
        write(n, "scores.csv", h, [(3, 0.90, "09:05"), (1, 0.5000000001, "09:05"), (2, 0.71, "09:05"), (4, 0.1, "09:05")])
        write(o, "churn.csv", ["id", "p"], [(1, 0.2)]); write(n, "extra.csv", ["id", "p"], [(1, 0.2)])
        res = compare_dirs(o, n)
    print("\n".join(res) if res else "IDENTICAL within tolerance")
    print(f"diffs: {len(res)}")
    sys.exit(1 if res else 0)
