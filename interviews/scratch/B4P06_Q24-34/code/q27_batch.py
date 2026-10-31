# Q27: chunked, resumable, atomic batch scorer (CSV -> parts -> ONNX). Run: q27_batch.py MODEL WORKDIR [--crash-after N]
import csv, os, sys, json, time, argparse
import numpy as np, onnxruntime as ort
ap = argparse.ArgumentParser(); ap.add_argument("model"); ap.add_argument("work")
ap.add_argument("--rows", type=int, default=100_000); ap.add_argument("--chunk", type=int, default=10_000)
ap.add_argument("--crash-after", type=int, default=None); a = ap.parse_args()
inp = os.path.join(a.work, "input.csv"); out_dir = os.path.join(a.work, "scores", "dt=2026-10-26")
os.makedirs(out_dir, exist_ok=True)
if not os.path.exists(inp):                       # generate input once
    rng = np.random.default_rng(7)
    X = np.round(rng.uniform([4,2,1,0.1],[8,4.5,7,2.5], size=(a.rows,4)), 2)
    with open(inp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id","f1","f2","f3","f4"])
        for i, r in enumerate(X): w.writerow([i, *r])
sess = ort.InferenceSession(a.model, providers=["CPUExecutionProvider"])   # load ONCE
def read_chunks(path, n):
    with open(path, newline="") as f:
        rd = csv.reader(f); next(rd); buf = []
        for row in rd:
            buf.append(row)
            if len(buf) == n: yield buf; buf = []
        if buf: yield buf
done = skipped = 0; t0 = time.perf_counter()
for k, rows in enumerate(read_chunks(inp, a.chunk)):
    final = os.path.join(out_dir, f"part-{k:05d}.csv")
    if os.path.exists(final): skipped += len(rows); continue          # resume: finished parts are skipped
    ids = [r[0] for r in rows]; x = np.array([r[1:] for r in rows], dtype=np.float32)
    labels = sess.run(["label"], {"X": x})[0]                         # vectorised
    tmp = final + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["id","label"]); w.writerows(zip(ids, labels.tolist()))
    os.replace(tmp, final)                                            # atomic rename
    done += len(rows)
    if a.crash_after is not None and k + 1 == a.crash_after: print("simulated crash after part", k); sys.exit(3)
# validate: counts + unique ids
total = 0; seen = set()
for fn in sorted(os.listdir(out_dir)):
    if fn.endswith(".tmp"): print("stray tmp file", fn); continue
    with open(os.path.join(out_dir, fn)) as f:
        rd = csv.reader(f); next(rd)
        for r in rd: total += 1; seen.add(r[0])
with open(inp) as f: n_in = sum(1 for _ in f) - 1
print(f"scored now {done}, skipped (already done) {skipped}, output rows {total}, unique ids {len(seen)}, input rows {n_in}, match {total==n_in==len(seen)}")
print("parts:", len([f for f in os.listdir(out_dir) if f.endswith('.csv')]), f"elapsed {time.perf_counter()-t0:.1f}s (this sandbox)")
