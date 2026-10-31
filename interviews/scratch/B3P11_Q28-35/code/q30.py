# Q30: pandas groupby/merge/query/sort choices. Timings: median of 5 repeats, machine-specific.
import sqlite3, time, warnings
import numpy as np
import pandas as pd

rng = np.random.default_rng(30)
n = 500_000
df = pd.DataFrame({"key": rng.integers(0, 1000, n),
                   "cat": pd.Categorical(np.array(list("abcd"))[rng.integers(0, 4, n)]),
                   "value": rng.normal(0, 1, n)})
lookup = pd.DataFrame({"key": np.arange(1000), "label": [f"L{i:04d}" for i in range(1000)]})

def t(fn, rep=5):
    xs = []
    fn()   # warm-up call, not timed
    for _ in range(rep):
        s = time.perf_counter(); r = fn(); xs.append(time.perf_counter() - s)
    return r, 1000 * float(np.median(xs))

def row(name, ms): print(f"  {name:<44}{ms:9.2f} ms")

print("1. add one lookup column")
m, ms1 = t(lambda: df.merge(lookup, on="key", how="left")); row("merge(how='left')", ms1)
mp, ms2 = t(lambda: df.assign(label=df["key"].map(lookup.set_index("key")["label"]))); row("Series.map on a keyed Series", ms2)
assert (m["label"].to_numpy() == mp["label"].to_numpy()).all() and len(m) == len(df)
print("   merge keeps row order for how='left' here:", bool((m["key"].to_numpy() == df["key"].to_numpy()).all()))
dup = pd.concat([lookup, lookup.iloc[:1]])
print("   duplicate key in lookup: merge rows", len(df.merge(dup, on="key", how="left")) - len(df), "extra;",
      "map raises:", end=" ")
try:
    df["key"].map(dup.set_index("key")["label"])
except Exception as e:
    print(type(e).__name__)

print("2. groupby sort")
g1, a = t(lambda: df.groupby("key")["value"].sum()); row("groupby('key', sort=True).sum", a)
g2, b = t(lambda: df.groupby("key", sort=False)["value"].sum()); row("groupby('key', sort=False).sum", b)
pd.testing.assert_series_equal(g1, g2.sort_index())
print("   same values after sort_index(); sort=False order is first appearance:", g2.index[:3].tolist())

print("3. groupby on the category column")
c1, a = t(lambda: df.groupby("cat", observed=True)["value"].sum()); row("category, observed=True", a)
c2, b = t(lambda: df.groupby("cat", observed=False)["value"].sum()); row("category, observed=False", b)
c3, c = t(lambda: df.assign(cs=df["cat"].astype(str)).groupby("cs")["value"].sum()); row("same column as str (incl. astype)", c)
pd.testing.assert_series_equal(c1, c2)
print("   default equals observed=True in 3.0.5:", c1.equals(df.groupby("cat")["value"].sum()),
      "| with an unused category observed=False adds a zero row:",
      df.assign(cat=df["cat"].cat.add_categories("z")).groupby("cat", observed=False)["value"].sum().loc["z"])

print("4. filter: mask vs query vs eval")
q1, a = t(lambda: df[(df["value"] > 0.5) & (df["key"] < 500)]); row("boolean mask", a)
q2, b = t(lambda: df.query("value > 0.5 and key < 500")); row("df.query", b)
q3, c = t(lambda: df[df.eval("value > 0.5 and key < 500")]); row("df[df.eval(...)]", c)
pd.testing.assert_frame_equal(q1, q2); pd.testing.assert_frame_equal(q1, q3)
small = df.iloc[:20_000]
_, a2 = t(lambda: small[(small["value"] > 0.5) & (small["key"] < 500)], 15)
_, b2 = t(lambda: small.query("value > 0.5 and key < 500"), 15)
print(f"   20,000 rows: mask {a2:.2f} ms vs query {b2:.2f} ms")
e1, a = t(lambda: df["value"] * 2 + df["key"]); row("arithmetic with plain operators", a)
e2, b = t(lambda: df.eval("value * 2 + key")); row("df.eval('value * 2 + key')", b)
assert np.allclose(e1, e2)

print("5. top k")
s1, a = t(lambda: df.sort_values("value", ascending=False).head(10)); row("sort_values(...).head(10)", a)
s2, b = t(lambda: df.nlargest(10, "value")); row("nlargest(10, 'value')", b)
assert s1["value"].tolist() == s2["value"].tolist()
print("   top value:", round(s2["value"].iloc[0], 4))

print("6. index-aligned vs column operation")
x = df["value"]; y = df["value"].sample(frac=1, random_state=1)    # same index labels, shuffled order
r1, a = t(lambda: x + y); row("x + y with the shuffled labels (aligns)", a)
r2, b = t(lambda: x + y.sort_index()); row("x + y.sort_index() (aligned, same order)", b)
r3, c = t(lambda: x.to_numpy() + y.to_numpy()); row("numpy: positional add (WRONG pairing)", c)
assert r1.equals(r2) and not np.allclose(r1.to_numpy(), r3)
print("   alignment pairs by label, positional add pairs by position: results differ (asserted)")

# SQL cross-check of the merge and groupby
con = sqlite3.connect(":memory:")
df.assign(cat=df["cat"].astype(str)).to_sql("t", con, index=False); lookup.to_sql("lk", con, index=False)
sj = pd.read_sql("SELECT t.key, lk.label FROM t LEFT JOIN lk ON lk.key = t.key", con)
assert sorted(sj["label"]) == sorted(m["label"])
sg = pd.read_sql("SELECT key, SUM(value) AS v FROM t GROUP BY key ORDER BY key", con).set_index("key")["v"]
assert np.allclose(sg.to_numpy(), g1.to_numpy())
con.close()
print("\nSQL LEFT JOIN labels and GROUP BY key sums equal pandas (sorted by key / label)")

print("\n7. chained assignment under pandas", pd.__version__)
d = pd.DataFrame({"a": [-1, 2, 3], "b": [0, 0, 0]})
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    d[d.a > 0]["b"] = 1
print("   after d[d.a > 0]['b'] = 1:", d["b"].tolist(), "| warnings:", [f"{x.category.__name__}" for x in w])
if w: print("   warning text:", str(w[0].message)[:230].replace("\n", " "))
d.loc[d.a > 0, "b"] = 1
print("   after d.loc[d.a > 0, 'b'] = 1:", d["b"].tolist())
sub = d[d.a > 0]; sub.loc[:, "b"] = 99
print("   writing to a filtered copy leaves the parent alone:", d["b"].tolist(), "| copy:", sub["b"].tolist())
