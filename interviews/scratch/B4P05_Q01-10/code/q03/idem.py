import csv, json, os, tempfile, pathlib

root = pathlib.Path(tempfile.mkdtemp())
rows = {"2026-10-01": [("u1", 10), ("u2", 20)]}

# BAD: append on every run
def bad(day, path):
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        for u, v in rows[day]:
            w.writerow([day, u, v])

# FIX 1: partition keyed by the interval, overwrite via temp file + atomic rename
def good_partition(day, base):
    part = base / f"dt={day}"
    part.mkdir(parents=True, exist_ok=True)
    tmp = part / "data.csv.tmp"
    with open(tmp, "w", newline="") as f:
        csv.writer(f).writerows([[day, u, v] for u, v in rows[day]])
    os.replace(tmp, part / "data.csv")   # atomic on the same filesystem

# FIX 2: upsert on a business key
def good_upsert(day, path):
    state = json.loads(path.read_text()) if path.exists() else {}
    for u, v in rows[day]:
        state[f"{day}|{u}"] = v          # same key -> same slot
    path.write_text(json.dumps(state, sort_keys=True))

def count_lines(p): return sum(1 for _ in open(p))

bad_path = root / "bad.csv"
for _ in range(2): bad("2026-10-01", bad_path)
print("BAD   rows after 2 runs:", count_lines(bad_path))

for _ in range(2): good_partition("2026-10-01", root / "tbl")
print("GOOD1 rows after 2 runs:", count_lines(root / "tbl/dt=2026-10-01/data.csv"),
      "| leftover tmp files:", [p.name for p in (root/"tbl/dt=2026-10-01").glob("*.tmp")])

up = root / "up.json"
for _ in range(2): good_upsert("2026-10-01", up)
print("GOOD2 keys after 2 runs:", len(json.loads(up.read_text())), json.loads(up.read_text()))

# side effects: guard with a ledger
sent = root / "sent.txt"
def notify(run_key):
    done = sent.read_text().split() if sent.exists() else []
    if run_key in done:
        return "skipped (already sent)"
    sent.write_text(" ".join(done + [run_key]))
    return "sent"
print("email run 1:", notify("train|2026-10-01"))
print("email run 2:", notify("train|2026-10-01"))
