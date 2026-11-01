# NULL-aware data-quality audit: one row per column, built from PRAGMA table_info.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER, name TEXT, email TEXT, phone TEXT, city TEXT, signup_date TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@x.com','98100 00001','Pune','2024-01-05'),
 (2,'Ben','ben@y.com','','Delhi','2024-01-09'),
 (3,'Chitra',NULL,'N/A','Pune','NULL'),
 (4,'Dev','dev@x.com','   ','Goa',''),
 (5,'  ','DEV@x.com',NULL,'pune','2024-02-01'),
 (6,NULL,'n/a','98100 00006','Delhi',NULL),
 (7,'Gita','gita@z.com','98100 00007','NULL','2024-02-11'),
 (8,'Hari','asha@x.com','98100 00008','','2024-02-20');
""")
PLACEHOLDERS = ("N/A", "NA", "NULL", "NONE", "-")
ph = ",".join("'" + p + "'" for p in PLACEHOLDERS)

cols = [r[1] for r in con.execute("PRAGMA table_info(customers)")]       # column names from the catalog
def one_col(c):
    q = '"' + c + '"'                                                    # quoted identifier
    return f"""SELECT '{c}' AS column_name,
  COUNT(*) AS total_rows,
  COUNT(*) - COUNT({q}) AS null_count,
  SUM({q} = '') AS empty_count,
  SUM({q} IS NOT NULL AND {q} <> '' AND trim({q}) = '') AS whitespace_only,
  SUM({q} IS NOT NULL AND upper(trim({q})) IN ({ph})) AS placeholder_count,
  COUNT(DISTINCT {q}) AS distinct_count,
  SUM({q} IS NULL OR trim({q}) = '' OR upper(trim({q})) IN ({ph})) AS effectively_missing,
  round(100.0 * SUM({q} IS NULL OR trim({q}) = '' OR upper(trim({q})) IN ({ph})) / COUNT(*), 1) AS pct_missing
FROM customers"""
audit_sql = "\nUNION ALL\n".join(one_col(c) for c in cols)
print(one_col("phone"))
sql_audit = pd.read_sql(audit_sql, con)
print(sql_audit.to_string(index=False))

# COUNT(*) - COUNT(col) versus effectively missing
print("phone: COUNT(*)-COUNT(phone) =", con.execute("SELECT COUNT(*)-COUNT(phone) FROM customers").fetchone()[0],
      "| effectively missing =", int(sql_audit.loc[sql_audit.column_name == "phone", "effectively_missing"].iloc[0]))

# duplicate keys: customer_id exact, email after normalisation, ignoring missing values
print("duplicate customer_id:", con.execute("SELECT customer_id FROM customers GROUP BY customer_id HAVING COUNT(*) > 1").fetchall())
print("duplicate emails (lower+trim, missing excluded):", con.execute("""
  SELECT lower(trim(email)) AS e, group_concat(customer_id, ',' ORDER BY customer_id)
  FROM customers WHERE email IS NOT NULL AND trim(email) <> '' AND upper(trim(email)) NOT IN ('N/A','NA','NULL','NONE','-')
  GROUP BY lower(trim(email)) HAVING COUNT(*) > 1""").fetchall())

# ---- pandas: same audit
df = pd.read_sql("SELECT * FROM customers", con)
rows = []
for c in df.columns:
    s = df[c]
    if pd.api.types.is_numeric_dtype(s):
        empty = ws = ph_n = 0
        miss = int(s.isna().sum())
    else:
        stripped = s.str.strip()
        empty = int((s == "").sum())
        ws = int(((stripped == "") & (s != "")).sum())
        ph_n = int(stripped.str.upper().isin(PLACEHOLDERS).sum())
        miss = int((s.isna() | (stripped == "") | stripped.str.upper().isin(PLACEHOLDERS)).sum())
    rows.append({"column_name": c, "total_rows": len(s), "null_count": int(s.isna().sum()), "empty_count": empty,
                 "whitespace_only": ws, "placeholder_count": ph_n, "distinct_count": int(s.nunique()),
                 "effectively_missing": miss, "pct_missing": round(100.0 * miss / len(s), 1)})
p_audit = pd.DataFrame(rows)
pd.testing.assert_frame_equal(p_audit, sql_audit, check_dtype=False)     # compared in column order
print("pandas audit equals SQL audit")
long = p_audit.melt(id_vars="column_name", var_name="metric", value_name="value")
print(long[long["metric"].isin(["effectively_missing", "pct_missing"])].to_string(index=False))

# honest differences
print("NBSP-only phone: SQL trim =", con.execute("SELECT length(trim(char(160)))").fetchone()[0], "(not whitespace), pandas strip ->",
      repr(pd.Series([" "]).str.strip()[0]))
print("printf('%.0f') of 12.5, 2.5, 2.9, 3.5, 100.6:", con.execute("SELECT printf('%.0f',12.5), printf('%.0f',2.5), printf('%.0f',2.9), printf('%.0f',3.5), printf('%.0f',100.6)").fetchone())
print("round() of the same:", con.execute("SELECT round(12.5), round(2.5), round(2.9), round(3.5), round(100.6)").fetchone(),
      "| printf('%.0f', round(x)):", con.execute("SELECT printf('%.0f',round(2.9)), printf('%.0f',round(100.6))").fetchone(),
      "| Python '%.0f' % 2.5, 3.5, 2.9:", ["%.0f" % 2.5, "%.0f" % 3.5, "%.0f" % 2.9])
con.close()
print("asserts passed")
