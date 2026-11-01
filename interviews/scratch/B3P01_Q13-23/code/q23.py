# GROUP BY / ORDER BY ordinals and aliases (Q23), plus pandas value_counts and groupby().size().
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'completed'),(3,'completed'),(4,'cancelled'),(5,'cancelled'),
 (6,'refunded'),(7,'pending'),(8,NULL),(9,NULL);
""")

q = "SELECT status, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC, 1"
q_alias = "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC, status"
print("GROUP BY 1 ORDER BY 2 DESC, 1:", con.execute(q).fetchall())
assert con.execute(q).fetchall() == con.execute(q_alias).fetchall()

# fragility: reorder the SELECT list and the ordinal silently points at another column
frag = "SELECT COUNT(*) AS n, status FROM orders GROUP BY 1 ORDER BY 2"
print("reordered SELECT, ordinals updated by hand (correct):", con.execute("SELECT COUNT(*) AS n, status FROM orders GROUP BY 2 ORDER BY 1 DESC, 2").fetchall())
# someone inserts a column before COUNT(*): ORDER BY 2 now silently sorts by first_id, no error
print("column inserted, ORDER BY 2 left alone (silently wrong):",
      con.execute("SELECT status, MIN(order_id) AS first_id, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC").fetchall())
try:
    print(con.execute(frag).fetchall())
except sqlite3.Error as e:
    print("reordered SELECT but GROUP BY 1 not updated (column 1 is now COUNT(*)) ->", type(e).__name__, e)
try:
    con.execute("SELECT status, COUNT(*) FROM orders GROUP BY 1 ORDER BY 3")
except sqlite3.Error as e:
    print("ORDER BY 3 with two columns ->", type(e).__name__, e)

# alias in GROUP BY, alias of an expression
q_expr = "SELECT LENGTH(COALESCE(status,'')) AS len, COUNT(*) AS n FROM orders GROUP BY len ORDER BY len"
print("alias of an expression in GROUP BY (SQLite accepts):", con.execute(q_expr).fetchall())

# pandas: three equivalents. value_counts and groupby both drop NaN by default; SQL keeps the NULL group.
orders = pd.read_sql("SELECT * FROM orders", con)
sql_df = pd.read_sql(q, con)
v = (orders["status"].value_counts(dropna=False).rename("n").rename_axis("status").reset_index()
     .sort_values(["n", "status"], ascending=[False, True], na_position="first").reset_index(drop=True))
g = (orders.groupby("status", dropna=False).size().rename("n").reset_index()
     .sort_values(["n", "status"], ascending=[False, True], na_position="first").reset_index(drop=True))
print("value_counts() default (NaN dropped):", orders["status"].value_counts().to_dict())
print("groupby().size() default (NaN dropped):", orders.groupby("status").size().to_dict())
print(g.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, v)
pd.testing.assert_frame_equal(sql_df, g)
print("asserts passed (n DESC, status ASC tie-break; NULL status sorts first inside the tie, as in SQLite)")
