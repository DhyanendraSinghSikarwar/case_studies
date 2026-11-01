# Q36: three-or-more-in-a-row checks in pandas: rolling, run keys, np.diff, itertools.groupby (+ SQL window frame)
import itertools
import sqlite3
import time
import numpy as np
import pandas as pd

flags = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]
s = pd.Series(flags, name="flag")

# pd:main
end3 = s.rolling(3).min().eq(1)                                   # True only on the LAST row of each 3-window
in_run = end3[::-1].rolling(3, min_periods=1).max().astype(bool)[::-1]   # spread back over the next 2 rows
key = (s != s.shift()).cumsum()                                   # run key
size = s.groupby(key).transform("size")
in_run_key = s.eq(1) & size.ge(3)
# pd:end
print("flag      :", flags)
print("end3      :", end3.astype(int).tolist())
print("in_run    :", in_run.astype(int).tolist())
print("in_run key:", in_run_key.astype(int).tolist())
assert in_run.equals(in_run_key)

# forward-looking window object gives the same mask
fwd = pd.api.indexers.FixedForwardWindowIndexer(window_size=3)
start3 = s.rolling(fwd).min().eq(1)                               # True on the FIRST row of each 3-window
in_run_fwd = (end3.astype(int) | start3.astype(int)).astype(bool)
mid = s.rolling(3, center=True).min().eq(1)
in_run_all = (end3 | start3 | mid)
assert in_run_all.equals(in_run_key)
print("end|start|centre windows equal the run-size mask:", True)

# np.diff on the padded flag array: starts and ends of every run of ones
a = np.asarray(flags)
d = np.diff(np.concatenate(([0], a, [0])))
starts = np.flatnonzero(d == 1); ends = np.flatnonzero(d == -1)    # end index is exclusive
lengths = ends - starts
print("np.diff runs (start, length):", list(zip(starts.tolist(), lengths.tolist())))
mask_np = np.zeros(len(a), dtype=bool)
for st, ln in zip(starts, lengths):
    if ln >= 3:
        mask_np[st:st + ln] = True
assert (mask_np == in_run_key.to_numpy()).all()

# itertools.groupby for the longest run of ones
runs = [(k, len(list(g))) for k, g in itertools.groupby(flags)]
longest_it = max(n for k, n in runs if k == 1)
print("itertools runs:", runs, "longest run of ones:", longest_it)
assert longest_it == int(lengths.max()) == int(size[s.eq(1)].max())

# SQL: the same rolling check as a window frame
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE f(pos INTEGER, flag INTEGER)")
con.executemany("INSERT INTO f VALUES (?, ?)", list(enumerate(flags)))
SQL_MAIN = """
WITH e AS (
  SELECT pos, flag,
         CASE WHEN COUNT(flag) OVER w3 = 3 AND MIN(flag) OVER w3 = 1 THEN 1 ELSE 0 END AS end3
  FROM f
  WINDOW w3 AS (ORDER BY pos ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
)
SELECT pos, MAX(end3) OVER (ORDER BY pos ROWS BETWEEN CURRENT ROW AND 2 FOLLOWING) AS in_run
FROM e
ORDER BY pos
"""
sql_mask = [r[1] for r in con.execute(SQL_MAIN)]
print("SQL in_run:", sql_mask)
assert sql_mask == in_run_key.astype(int).tolist()

# NaN in the first rows and min_periods
sn = pd.Series([np.nan, 1, 1, 1, 1, 0, 1, 1, np.nan, 1, 1, 1], dtype="float64")
print("with NaN, default min_periods :", sn.rolling(3).min().eq(1).astype(int).tolist())
print("with NaN, min_periods=1 (wrong):", sn.rolling(3, min_periods=1).min().eq(1).astype(int).tolist())
print("rolling(3).min() raw:", sn.rolling(3).min().tolist())
# dtype of results
print("dtypes: rolling min", s.rolling(3).min().dtype, "| eq(1)", end3.dtype, "| bool input ->",
      s.astype(bool).rolling(3).min().dtype)

# speed on a large series (best of 3; this machine only, not a benchmark claim)
rng = np.random.default_rng(0)
big = pd.Series((rng.random(1_000_000) < 0.7).astype(int))
def t(fn):
    best = 1e9
    for _ in range(3):
        t0 = time.perf_counter(); fn(); best = min(best, time.perf_counter() - t0)
    return round(best * 1000, 1)
def m_roll():
    e = big.rolling(3).min().eq(1)
    return e[::-1].rolling(3, min_periods=1).max().astype(bool)[::-1]
def m_key():
    k = (big != big.shift()).cumsum()
    return big.eq(1) & big.groupby(k).transform("size").ge(3)
def m_np():
    x = big.to_numpy(); dd = np.diff(np.concatenate(([0], x, [0])))
    return np.flatnonzero(dd == 1), np.flatnonzero(dd == -1)
def m_it():
    return max((len(list(g)) for k, g in itertools.groupby(big.tolist()) if k == 1), default=0)
r1, r2 = m_roll(), m_key()
assert r1.equals(r2)
print("1,000,000 rows, ms (best of 3): rolling", t(m_roll), "| shift-key groupby", t(m_key),
      "| np.diff", t(m_np), "| itertools.groupby (longest only)", t(m_it))
print("asserts passed")
