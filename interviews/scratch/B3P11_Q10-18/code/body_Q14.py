import time
rng = np.random.default_rng(14)
N = 200000
df = pd.DataFrame({"a": rng.integers(1, 100, N), "b": rng.uniform(0, 10, N).round(3),
                   "s": rng.choice(["red", "green", "blue", "amber"], N)})
print(df.dtypes.to_dict())

def timed(fn, repeat=3):
    best = None
    for _ in range(repeat):
        t0 = time.perf_counter(); out = fn(); dt = time.perf_counter() - t0
        best = dt if best is None or dt < best else best
    return out, best * 1000

vec, t_vec = timed(lambda: df.a * df.b)
app, t_app = timed(lambda: df.apply(lambda r: r["a"] * r["b"], axis=1), repeat=1)
itr, t_itr = timed(lambda: [r["a"] * r["b"] for _, r in df.iterrows()], repeat=1)
tup, t_tup = timed(lambda: [t.a * t.b for t in df.itertuples(index=False)])
zp, t_zip = timed(lambda: [x * y for x, y in zip(df.a, df.b)])
mp, t_map = timed(lambda: df.a.map(lambda x: x * 2.5))
arr, t_np = timed(lambda: df.a.to_numpy() * df.b.to_numpy())
for name, out in [("apply", app), ("iterrows", itr), ("itertuples", tup), ("zip", zp)]:
    assert np.allclose(np.asarray(out, dtype=float), vec.to_numpy()), name
assert np.allclose(arr, vec.to_numpy())
assert np.allclose(mp.to_numpy(), df.a.to_numpy() * 2.5)
print("machine-specific timings in ms (best of 3 where cheap, one run for apply and iterrows):")
for k, v in sorted({"vectorised a*b": t_vec, "numpy arrays": t_np, "zip loop": t_zip, "itertuples": t_tup,
                    "Series.map(lambda)": t_map, "apply(axis=1)": t_app, "iterrows": t_itr}.items(), key=lambda kv: kv[1]):
    print(f"   {k:<20}{v:>10.1f}")
print("ratios vs vectorised: apply x%.0f, iterrows x%.0f, itertuples x%.0f" % (t_app / t_vec, t_itr / t_vec, t_tup / t_vec))

print("--- iterrows builds a Series per row and upcasts ---")
small = pd.DataFrame({"i": [1, 2], "x": [0.5, 1.5], "t": ["u", "v"]})
for idx, row in small.iterrows():
    print("   row dtype:", row.dtype, "| row['i'] =", repr(row["i"]), type(row["i"]).__name__)
    break
print("   itertuples keeps types:", [type(v).__name__ for v in next(small.itertuples(index=False))])
numeric = pd.DataFrame({"i": [1, 2], "x": [0.5, 1.5]})
print("   numeric-only iterrows: row dtype", next(numeric.iterrows())[1].dtype, "(int 1 became float)")

print("--- when you cannot vectorise a formula, push the branching into numpy ---")
cond = [df.a < 20, df.a < 60]
sel, t_sel = timed(lambda: np.select(cond, [df.b * 1.0, df.b * 1.5], default=df.b * 2.0))
def tiered(a, b):
    return b if a < 20 else (b * 1.5 if a < 60 else b * 2.0)
lp, t_lp = timed(lambda: [tiered(a, b) for a, b in zip(df.a, df.b)])
vz, t_vz = timed(lambda: np.vectorize(tiered)(df.a, df.b), repeat=1)
assert np.allclose(sel, lp) and np.allclose(sel, vz)
print(f"   np.select {t_sel:.1f} ms | python loop {t_lp:.1f} ms | np.vectorize {t_vz:.1f} ms (np.vectorize is a loop, not speed)")

print("--- strings: .str.upper vs map(str.upper) vs apply ---")
u1, t1 = timed(lambda: df.s.str.upper())
u2, t2 = timed(lambda: df.s.map(str.upper))
u3, t3 = timed(lambda: df.s.apply(lambda v: v.upper()))
cat = df.s.astype("category")
u4, t4 = timed(lambda: cat.cat.rename_categories(str.upper))
assert u1.tolist() == u2.tolist() == u3.tolist() == u4.astype(str).tolist()
print(f"   .str.upper {t1:.1f} | map(str.upper) {t2:.1f} | apply(lambda) {t3:.1f} | category rename {t4:.1f}  (ms)")

print("--- SQL pushes the same arithmetic into the engine ---")
c = sqlite3.connect(":memory:")
df.to_sql("t", c, index=False)
sq = pd.read_sql("SELECT a * b AS ab FROM t", c).ab
assert np.allclose(sq.to_numpy(), vec.to_numpy())
print("SQL a*b equals pandas a*b for all", N, "rows")

print("--- eval/query ---")
m, tm = timed(lambda: df[(df.a > 50) & (df.b < 5)])
q, tq = timed(lambda: df.query("a > 50 and b < 5"))
assert m.equals(q)
print(f"   mask {tm:.1f} ms | query {tq:.1f} ms (200,000 rows, machine-specific)")
