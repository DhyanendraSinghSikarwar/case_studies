# Q23: padding, truncation and number formatting in SQLite (no LPAD/RPAD) versus pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE invoices(invoice_no INTEGER PRIMARY KEY, amount REAL, customer_name TEXT);
INSERT INTO invoices VALUES
 (42,     1234.5,      'Alexander Hamilton'),
 (7,      0.5,         'Bo'),
 (123456, 1234567.891, 'Christopher Robin'),
 (99999,  703.125,     'Dee'),
 (5,      NULL,        NULL);
""")

sql = """
SELECT invoice_no,
       'INV-' || SUBSTR('00000' || invoice_no, -5)                          AS code_substr,
       PRINTF('INV-%05d', invoice_no)                                       AS code_printf,
       PRINTF('%-10s|', customer_name)                                      AS name_left,
       CASE WHEN LENGTH(customer_name) > 10 THEN SUBSTR(customer_name, 1, 9) || '…' ELSE customer_name END AS name_trunc,
       PRINTF('%,.2f', amount)                                              AS amount_comma
FROM invoices ORDER BY invoice_no"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

print("negative number:", con.execute("SELECT 'INV-' || SUBSTR('00000' || -42, -5), PRINTF('INV-%05d', -42)").fetchone())
print("NULL: || gives", con.execute("SELECT 'N:' || NULL").fetchone()[0], "| printf %s gives", repr(con.execute("SELECT PRINTF('%s', NULL)").fetchone()[0]),
      "| printf %d gives", repr(con.execute("SELECT PRINTF('%d', NULL)").fetchone()[0]))
print("right-justify:", repr(con.execute("SELECT PRINTF('%10s', 'abc')").fetchone()[0]))

# rounding: ROUND versus PRINTF, and Python/pandas
q = con.execute("""SELECT ROUND(703.125, 2), PRINTF('%.2f', 703.125), ROUND(2.675, 2), PRINTF('%.2f', 2.675),
                          ROUND(1.005, 2), PRINTF('%.2f', 1.005), ROUND(0.125, 2), PRINTF('%.2f', 0.125)""").fetchone()
print("SQLite ROUND/PRINTF 703.125, 2.675, 1.005, 0.125:", q)
print("Python round / format 703.125, 2.675, 1.005, 0.125:",
      (round(703.125, 2), f"{703.125:.2f}", round(2.675, 2), f"{2.675:.2f}", round(1.005, 2), f"{1.005:.2f}", round(0.125, 2), f"{0.125:.2f}"))
print("pandas Series.round(2) of the same four:", pd.Series([703.125, 2.675, 1.005, 0.125]).round(2).tolist())
print("PRINTF('%.0f') of 0.6, 1.6, 2.5, 2.6:", con.execute("SELECT PRINTF('%.0f',0.6), PRINTF('%.0f',1.6), PRINTF('%.0f',2.5), PRINTF('%.0f',2.6)").fetchone(),
      "| ROUND first:", con.execute("SELECT PRINTF('%.0f',ROUND(0.6)), PRINTF('%.0f',ROUND(1.6)), PRINTF('%.0f',ROUND(2.5)), PRINTF('%.0f',ROUND(2.6))").fetchone())

# pandas
p = pd.read_sql("SELECT * FROM invoices ORDER BY invoice_no", con)
pd_df = pd.DataFrame({
    "invoice_no": p["invoice_no"],
    "code_substr": "INV-" + p["invoice_no"].astype(str).str.zfill(5).str[-5:],          # same cut as SUBSTR(...,-5)
    "code_printf": p["invoice_no"].map(lambda n: f"INV-{n:05d}"),
    "name_left": p["customer_name"].str.ljust(10) + "|",
    "name_trunc": p["customer_name"].where(p["customer_name"].str.len() <= 10, p["customer_name"].str[:9] + "…"),
    "amount_comma": p["amount"].map(lambda x: None if pd.isna(x) else f"{x:,.2f}"),
})
print("SQL PRINTF('%,.2f', NULL):", repr(con.execute("SELECT PRINTF('%,.2f', NULL)").fetchone()[0]))
print("pad/justify/zfill in pandas:", pd.Series([7]).astype(str).str.zfill(5).tolist(), pd.Series(["ab"]).str.pad(6, side="left").tolist(),
      pd.Series(["-42"]).str.zfill(5).tolist())

def norm(df):
    return [tuple(None if (not isinstance(v, str) and pd.isna(v)) else v for v in row) for row in df.itertuples(index=False)]

s_rows, p_rows = norm(sql_df), norm(pd_df)
# the amount 703.125 row differs on purpose: SQLite rounds the exact tie up, Python's format rounds half to even
tie = [i for i, r in enumerate(s_rows) if r[0] == 99999][0]
assert s_rows[tie][5] == "703.13" and p_rows[tie][5] == "703.12"
for i, (a, b) in enumerate(zip(s_rows, p_rows)):
    if a[0] == 5:                      # NULL row: SQL PRINTF turns NULL into '' / 0.00, pandas keeps NaN (None here)
        assert a[3] == "          |" and b[3] is None and a[5] == "0.00" and b[5] is None
        continue
    cols = range(5) if i == tie else range(6)
    assert all(a[j] == b[j] for j in cols), (a, b)
print("asserts passed (SQL == pandas on every cell, except the two documented differences: the 703.125 tie and the NULL row)")
