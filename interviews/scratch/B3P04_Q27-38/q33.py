# Q33: qcut versus NTILE (and cut)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE spend(cust_id INTEGER PRIMARY KEY, amount INTEGER);
INSERT INTO spend VALUES (1,10),(2,20),(3,20),(4,20),(5,30),(6,40),(7,40),(8,50),(9,60),(10,100);
"""
SQL_MAIN = """
SELECT cust_id, amount,
       NTILE(4) OVER (ORDER BY amount, cust_id) AS ntile4
FROM spend
ORDER BY cust_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
spend = pd.read_sql_query("SELECT * FROM spend ORDER BY cust_id", con)
# pd:main
x = spend["amount"]
k = 4
pos = x.rank(method="first")                                  # 1..n, ties broken by row order (cust_id order)
n = len(x)
q, r = divmod(n, k)                                           # NTILE: first r buckets get q+1 rows
big = r * (q + 1)
ntile_pd = np.where(pos <= big, np.ceil(pos / (q + 1)), r + np.ceil((pos - big) / q)).astype("int64")
qcut_vals = pd.qcut(x, k, labels=False) + 1                   # cuts on quantile VALUES
qcut_rank = pd.qcut(pos, k, labels=False) + 1                 # qcut on positions
cut_vals = pd.cut(x, k, labels=False) + 1                     # equal-WIDTH bins
# pd:end
res = spend.assign(ntile4_sql=sql_df["ntile4"], ntile_pd=ntile_pd, qcut=qcut_vals, qcut_on_rank=qcut_rank, cut=cut_vals)
print(res.to_string(index=False))
for c in ["ntile4_sql", "qcut", "qcut_on_rank", "cut"]:
    print(f"bucket sizes {c:13s}:", res[c].value_counts().sort_index().tolist())
print("qcut bin edges:", pd.qcut(x, k, retbins=True)[1].tolist())
print("cut  bin edges:", [round(float(v), 2) for v in pd.cut(x, k, retbins=True)[1]])
# compared in cust_id order (SQL ORDER BY cust_id, frame in cust_id order)
assert sql_df["ntile4"].tolist() == ntile_pd.tolist()
assert qcut_vals.tolist() != ntile_pd.tolist()
assert qcut_rank.tolist() != ntile_pd.tolist()

# other sizes: NTILE puts the extra rows first, qcut-on-position does not
for m in (7, 9, 10):
    c2 = sqlite3.connect(":memory:")
    c2.execute("CREATE TABLE t(v INTEGER)")
    c2.executemany("INSERT INTO t VALUES (?)", [(i,) for i in range(m)])
    nt = [r_[0] for r_ in c2.execute("SELECT NTILE(4) OVER (ORDER BY v) FROM t")]
    qc = (pd.qcut(pd.Series(range(m)), 4, labels=False) + 1).tolist()
    print(f"n={m}: NTILE sizes {np.bincount(nt)[1:].tolist()} | qcut sizes {np.bincount(qc)[1:].tolist()}")

# heavy ties: qcut raises unless duplicates='drop' (then fewer bins)
heavy = pd.Series([5, 5, 5, 5, 5, 1, 2, 9, 9, 10])
try:
    pd.qcut(heavy, 4, labels=False)
except ValueError as ex:
    print("\nqcut on heavy ties raises:", str(ex).splitlines()[0])
print("duplicates='drop' labels:", pd.qcut(heavy, 4, labels=False, duplicates="drop").tolist())
print("asserts passed: NTILE == pandas formula; qcut differs from NTILE on this data")
