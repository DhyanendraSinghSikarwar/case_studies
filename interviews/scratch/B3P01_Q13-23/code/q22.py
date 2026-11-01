# LIMIT/OFFSET pagination, its failure modes, and keyset (seek) pagination (Q22).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, created_at TEXT, amount INTEGER)")
# 30 orders, two per day (so created_at has ties): ids 1,2 on 2025-03-01; 3,4 on 2025-03-02; ... 29,30 on 2025-03-15
rows = [(i, f"2025-03-{(i - 1) // 2 + 1:02d}", 100 + 10 * i) for i in range(1, 31)]
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)

PAGE, N = 10, 3
page3 = f"SELECT order_id, created_at FROM orders ORDER BY created_at DESC, order_id DESC LIMIT {PAGE} OFFSET {(N - 1) * PAGE}"
r3 = con.execute(page3).fetchall()
print("page 3 (OFFSET 20):", [r[0] for r in r3])

page1 = "SELECT order_id FROM orders ORDER BY created_at DESC, order_id DESC LIMIT 10 OFFSET 0"
page2 = "SELECT order_id FROM orders ORDER BY created_at DESC, order_id DESC LIMIT 10 OFFSET 10"
p1 = [r[0] for r in con.execute(page1)]
print("page 1:", p1)

# a new order arrives between requests -> offset pages shift
con.execute("INSERT INTO orders VALUES (31,'2025-03-16',999)")
p2_after_insert = [r[0] for r in con.execute(page2)]
print("page 2 after a new order arrived:", p2_after_insert, "-> repeats", sorted(set(p1) & set(p2_after_insert)), "from page 1")
con.execute("DELETE FROM orders WHERE order_id = 31")

# ties: sort key without the tie-breaker (created_at only) can split a tie group unpredictably between pages
tie_q = "SELECT order_id FROM orders ORDER BY created_at DESC LIMIT 3 OFFSET {}"
print("created_at-only order, pages of 3 (engine's tie order, not guaranteed):",
      [[r[0] for r in con.execute(tie_q.format(o))] for o in (0, 3)])

# keyset (seek): continue after the last row of page 1 with a row-value comparison
last = con.execute("SELECT created_at, order_id FROM orders WHERE order_id = ?", (p1[-1],)).fetchone()
keyset_rv = ("SELECT order_id FROM orders WHERE (created_at, order_id) < (?, ?) "
             "ORDER BY created_at DESC, order_id DESC LIMIT 10")
keyset_or = ("SELECT order_id FROM orders WHERE created_at < ? OR (created_at = ? AND order_id < ?) "
             "ORDER BY created_at DESC, order_id DESC LIMIT 10")
k_rv = [r[0] for r in con.execute(keyset_rv, last)]
k_or = [r[0] for r in con.execute(keyset_or, (last[0], last[0], last[1]))]
print("keyset page 2 (row values):", k_rv)
print("keyset page 2 (expanded OR):", k_or)

# after a new row arrives, keyset page 2 is unchanged
con.execute("INSERT INTO orders VALUES (31,'2025-03-16',999)")
print("keyset page 2 after insert:", [r[0] for r in con.execute(keyset_rv, last)])
con.execute("DELETE FROM orders WHERE order_id = 31")

# pandas
df = pd.read_sql("SELECT * FROM orders", con)
ordered = df.sort_values(["created_at", "order_id"], ascending=False).reset_index(drop=True)
pp3 = ordered.iloc[(N - 1) * PAGE : N * PAGE]
print("pandas iloc[20:30]:", pp3["order_id"].tolist())
# nlargest then tail is the pandas docs' idiom for LIMIT/OFFSET (tail of the top 30 = rows 21-30)
# nlargest needs numeric or datetime columns, so convert the text date first
df2 = df.assign(day=pd.to_datetime(df["created_at"]))
nl = df2.nlargest(30, ["day", "order_id"]).tail(10)
print("nlargest(30, ['day','order_id']).tail(10):", nl["order_id"].tolist())
try:
    df.nlargest(3, "created_at")
except TypeError as e:
    print("nlargest on a text column ->", type(e).__name__, e)

assert [r[0] for r in r3] == pp3["order_id"].tolist() == nl["order_id"].tolist()
assert k_rv == k_or == [r[0] for r in con.execute(page2)] == ordered.iloc[10:20]["order_id"].tolist()
print("asserts passed (all compared in order, newest first with order_id tie-break)")
