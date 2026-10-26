# Q26: window sort cost and top-N per group plans
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

WIN = """SELECT region, sale_id, amount FROM (
  SELECT region, sale_id, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY region, amount DESC, sale_id"""
CNT = """SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE (SELECT COUNT(*) FROM sales b WHERE b.region = a.region
       AND (b.amount > a.amount OR (b.amount = a.amount AND b.sale_id < a.sale_id))) < 3
ORDER BY a.region, a.amount DESC, a.sale_id"""
INL = """SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE a.sale_id IN (SELECT b.sale_id FROM sales b WHERE b.region = a.region ORDER BY b.amount DESC, b.sale_id LIMIT 3)
ORDER BY a.region, a.amount DESC, a.sale_id"""
WIN_EXTRA = """SELECT region, sale_id, amount, sale_date FROM (
  SELECT region, sale_id, amount, sale_date, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY sale_date"""

def build(n, seed=26, regions=50):
    rnd = random.Random(seed)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER)")
    con.executemany("INSERT INTO sales VALUES (?,?,?,?,?)",
        [(i, "R%02d" % rnd.randint(1, regions), rnd.randint(1, 500), "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 3000)) for i in range(1, n + 1)])
    con.commit()
    return con

def pandas_top3(df):
    d = df.sort_values(["region", "amount", "sale_id"], ascending=[True, False, True])
    return d.groupby("region").head(3)[["region", "sale_id", "amount"]].reset_index(drop=True)

# tiny sample with a tie
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'N',1,'2024-01-01',50),(2,'N',2,'2024-01-02',90),(3,'N',3,'2024-01-03',90),(4,'N',4,'2024-01-04',70),(5,'N',5,'2024-01-05',10),
 (6,'S',1,'2024-01-06',20),(7,'S',2,'2024-01-07',30);""")
for nm, q in (("window", WIN), ("correlated COUNT", CNT), ("correlated IN + LIMIT", INL)):
    print("tiny", nm, t.execute(q).fetchall())
print("tiny: plain count form with only '>' would return", t.execute("""SELECT a.sale_id FROM sales a WHERE (SELECT COUNT(*) FROM sales b WHERE b.region=a.region AND b.amount > a.amount) < 3 AND a.region='N' ORDER BY 1""").fetchall(), "(ties at 90 both rank 0, 70 rank 2, 50 rank 3 excluded; tie-break matters when ranks collide)")

# same-size comparison of all forms at 6,000 rows (the correlated forms are too slow at 300,000 without early exit)
print("\n== 6,000 rows (50 regions x about 120 rows), all forms, with and without the index")
small = build(6000)
sdf = pd.read_sql("SELECT * FROM sales", small)
exp_s = pandas_top3(sdf)
for idx in (False, True):
    if idx:
        small.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)"); small.commit()
    for nm, q in (("window", WIN), ("correlated COUNT", CNT), ("correlated IN + LIMIT", INL)):
        rows, n = steps(small, q)
        pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_s)
        print("index=%-5s %-22s rows %3d VM steps %9d" % (idx, nm, len(rows), n))
        for l in plan(small, q): print("       ", l)

print("\n== quadratic growth of the correlated COUNT with the index (rows per region grows with n)")
for n in (3000, 6000, 12000):
    c = build(n); c.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)")
    print("  n=%6d steps %9d  steps/n = %.1f" % (n, steps(c, CNT)[1], steps(c, CNT)[1] / n))

print("\n== 300,000 rows")
big = build(300000)
bdf = pd.read_sql("SELECT * FROM sales", big)
exp_b = pandas_top3(bdf)
rows, n = steps(big, WIN)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("window, no index:                      rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, WIN): print("       ", l)
big.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)"); big.commit()
rows, n = steps(big, WIN)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("window, index (region, amount DESC, sale_id): rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, WIN): print("       ", l)
rows, n = steps(big, INL)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("correlated IN + LIMIT, index:           rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, INL): print("       ", l)
print("(correlated COUNT not run at 300,000 rows: it needs about n*rows-per-region/2 index entries, see the growth table)")

print("\n== an extra ORDER BY on another key (sale_date) after the window, 300,000 rows, index present")
rows, n = steps(big, WIN_EXTRA)
print("rows %d VM steps %d" % (len(rows), n))
pl = plan(big, WIN_EXTRA)
for l in pl: print("       ", l)
print("temp b-tree lines in this plan:", sum("TEMP B-TREE" in l for l in pl), "; in the WIN plan:", sum("TEMP B-TREE" in l for l in plan(big, WIN)))
print("asserts passed: all forms equal the pandas sort + groupby.head(3) (compared in order region, amount desc, sale_id)")
