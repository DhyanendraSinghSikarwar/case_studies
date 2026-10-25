# Q3: toy recursion with carried state: factorial, Fibonacci, powers of 2, digits; overflow behaviour in SQLite
import math
import sqlite3
import pandas as pd

SQL_FACT = """
WITH RECURSIVE f(n, fact) AS (
  SELECT 1, 1
  UNION ALL
  SELECT n + 1, fact * (n + 1) FROM f WHERE n < 10
)
SELECT n, fact FROM f ORDER BY n
"""
SQL_FIB = """
WITH RECURSIVE fib(n, fib, next_fib) AS (
  SELECT 1, 0, 1
  UNION ALL
  SELECT n + 1, next_fib, fib + next_fib FROM fib WHERE n < 15
)
SELECT n, fib FROM fib ORDER BY n
"""
SQL_POW = """
WITH RECURSIVE p(e, val) AS (
  SELECT 0, 1
  UNION ALL
  SELECT e + 1, val * 2 FROM p WHERE e < 20
)
SELECT e, val FROM p ORDER BY e
"""
SQL_DIGITS = """
WITH RECURSIVE d(pos, rest, digit) AS (
  SELECT 1, abs(:num) / 10, abs(:num) % 10          -- anchor: the last digit, so 0 still gives one row
  UNION ALL
  SELECT pos + 1, rest / 10, rest % 10 FROM d WHERE rest > 0
)
SELECT pos, digit FROM d ORDER BY pos DESC          -- pos 1 is the last digit; DESC reads left to right
"""
con = sqlite3.connect(":memory:")
sql_fact = pd.read_sql_query(SQL_FACT, con)
sql_fib = pd.read_sql_query(SQL_FIB, con)
sql_pow = pd.read_sql_query(SQL_POW, con)
sql_dig = pd.read_sql_query(SQL_DIGITS, con, params={"num": 90210})
print("factorial:", dict(zip(sql_fact["n"], sql_fact["fact"])))
print("fibonacci:", sql_fib["fib"].tolist())
print("powers of 2:", sql_pow["val"].tolist()[:6], "...", sql_pow["val"].iloc[-1])
print("digits of 90210 left to right:", sql_dig["digit"].tolist())

# pd:main
n = pd.Series(range(1, 11))
pd_fact = pd.DataFrame({"n": n, "fact": [math.factorial(int(k)) for k in n]})
fibs = [0, 1]
while len(fibs) < 15:
    fibs.append(fibs[-1] + fibs[-2])
pd_fib = pd.DataFrame({"n": range(1, 16), "fib": fibs})
pd_pow = pd.DataFrame({"e": range(21), "val": [2 ** k for k in range(21)]})
pd_dig = pd.DataFrame({"pos": range(5, 0, -1), "digit": [int(c) for c in str(90210)]})
# pd:end
pd.testing.assert_frame_equal(pd_fact, sql_fact, check_dtype=False)   # all four compared in the SQL ORDER BY order
pd.testing.assert_frame_equal(pd_fib, sql_fib, check_dtype=False)
pd.testing.assert_frame_equal(pd_pow, sql_pow, check_dtype=False)
pd.testing.assert_frame_equal(pd_dig, sql_dig, check_dtype=False)

# Edge cases for digits: 0 and a negative number
print("digits of 0:", [r[1] for r in con.execute(SQL_DIGITS, {"num": 0})], "| of -705:", [r[1] for r in con.execute(SQL_DIGITS, {"num": -705})])

# Overflow: run factorial to 25 and Fibonacci to 95 and watch typeof()
big = con.execute("""
WITH RECURSIVE f(n, fact) AS (SELECT 1, 1 UNION ALL SELECT n + 1, fact * (n + 1) FROM f WHERE n < 40)
SELECT n, typeof(fact), fact, printf('%.0f', fact) FROM f WHERE n IN (19, 20, 21, 22, 25, 30, 40)""").fetchall()
for n_, t, v, s in big:
    exact = math.factorial(n_)
    print(f"n={n_}: typeof={t}, value={v!r}, digits equal exact n!: {int(v) == exact}")
print("max signed 64-bit integer:", 2 ** 63 - 1, "| 20! =", math.factorial(20), "| 21! =", math.factorial(21))
fibx = [0, 1]
while len(fibx) < 100:
    fibx.append(fibx[-1] + fibx[-2])
fibt = con.execute("""
WITH RECURSIVE fib(n, a, b) AS (SELECT 1, 0, 1 UNION ALL SELECT n + 1, b, a + b FROM fib WHERE n < 95)
SELECT n, typeof(a), a FROM fib WHERE n IN (92, 93, 94, 95)""").fetchall()
for n_, t, v in fibt:
    print(f"row n={n_} holds F({n_ - 1}): typeof={t}, value={v!r}, exact={fibx[n_ - 1]}")
# integer overflow outside recursion
print("9223372036854775807 + 1 =", con.execute("SELECT 9223372036854775807 + 1, typeof(9223372036854775807 + 1)").fetchone())
# Python loop check against SQL to n=25 (relative tolerance once SQLite switches to float)
rows = con.execute("WITH RECURSIVE f(n, fact) AS (SELECT 1, 1 UNION ALL SELECT n + 1, fact * (n + 1) FROM f WHERE n < 25) SELECT n, fact FROM f").fetchall()
for n_, v in rows:
    assert math.isclose(float(v), float(math.factorial(n_)), rel_tol=1e-12)
    if n_ <= 20:
        assert v == math.factorial(n_)
print("asserts passed")
