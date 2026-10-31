# Q13: NULL vs '' vs blanks vs the text 'NULL' vs 0 (SQL and pandas)
import io
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, phone TEXT, city TEXT, credit_limit INTEGER);
INSERT INTO customers VALUES
 (1,'Asha','98765 43210','Pune',5000),
 (2,'Ben',NULL,'Delhi',NULL),
 (3,'Chitra','','Mumbai',0),
 (4,'Dev','   ','Pune',2000),
 (5,'Esha','NULL','Delhi',3000),
 (6,'Farid','N/A','Mumbai',NULL),
 (7,'Gita',' 98111 22222 ','Pune',1000),
 (8,'Hari',char(9),'Delhi',4000),      -- a tab only
 (9,'Ila',char(160),'Pune',0);         -- a no-break space only
""")

print("--- which predicate catches which row (1 = true, 0 = false, NULL = unknown) ---")
flags = pd.read_sql_query("""
SELECT customer_id AS id, quote(phone) AS stored, hex(phone) AS hex,
       IFNULL(phone IS NULL, 'NULL')                    AS is_null,
       IFNULL(phone = '', 'NULL')                       AS eq_empty,
       IFNULL(TRIM(phone) = '', 'NULL')                 AS trim_empty,
       IFNULL(phone = 'NULL', 'NULL')                   AS eq_text_null,
       IFNULL(NULLIF(TRIM(phone), '') IS NULL, 'NULL')  AS nullif_trim,
       IFNULL(phone <> '', 'NULL')                      AS ne_empty
FROM customers ORDER BY customer_id""", con)
print(flags.to_string(index=False))

# <<sql_norm
SQL_NORM = """
SELECT customer_id,
       CASE WHEN UPPER(TRIM(phone, ' ' || char(9) || char(10) || char(13) || char(160)))
                 IN ('', 'NULL', 'N/A', 'NA', 'NONE')
            THEN NULL
            ELSE TRIM(phone, ' ' || char(9) || char(10) || char(13) || char(160))
       END AS phone_clean
FROM customers ORDER BY customer_id
"""
# >>
# <<sql_counts
SQL_COUNTS = """
SELECT COUNT(*)                                   AS rows_total,
       COUNT(phone)                               AS count_phone,
       SUM(phone <> '')                           AS phone_ne_empty,
       (SELECT COUNT(phone_clean) FROM (""" + SQL_NORM.replace("ORDER BY customer_id", "") + """)) AS count_clean,
       AVG(credit_limit)                          AS avg_limit,
       AVG(COALESCE(credit_limit, 0))             AS avg_limit_null_as_0
FROM customers
"""
# >>
norm = pd.read_sql_query(SQL_NORM, con)
print("\nSQL normalised phone:"); print(norm.to_string(index=False))
counts = pd.read_sql_query(SQL_COUNTS, con)
print("\nSQL counts and averages:"); print(counts.to_string(index=False))
print("WHERE phone <> '' returns ids:", [r[0] for r in con.execute("SELECT customer_id FROM customers WHERE phone <> '' ORDER BY 1")])
print("WHERE phone IS NULL OR phone <> '' returns", con.execute("SELECT COUNT(*) FROM customers WHERE phone IS NULL OR phone <> ''").fetchone()[0], "rows")
print("WHERE TRIM(phone) = '' returns ids:", [r[0] for r in con.execute("SELECT customer_id FROM customers WHERE TRIM(phone) = '' ORDER BY 1")], "(tab and NBSP rows 8, 9 are missed)")

# <<pd_norm
df = pd.read_sql_query("SELECT * FROM customers ORDER BY customer_id", con)
clean = df["phone"].str.strip()                                   # pandas strip removes tab and NBSP too
p_norm = clean.mask(clean.str.upper().isin(["", "NULL", "N/A", "NA", "NONE"]))   # NaN stays NaN (isin gives False)
# >>
print("\npandas phone dtype:", df["phone"].dtype, "| isna count after normalising:", int(p_norm.isna().sum()))
print("pandas: mean skips NaN:", df["credit_limit"].mean(), "| fillna(0).mean():", df["credit_limit"].fillna(0).mean(),
      "| count(phone) before:", int(df["phone"].count()), "after:", int(p_norm.count()))

# match: compare by customer_id order, NULL == NaN
pd.testing.assert_series_equal(p_norm.reset_index(drop=True), norm["phone_clean"], check_names=False, check_dtype=False)
assert int(df["phone"].count()) == counts.loc[0, "count_phone"] == 8
assert int(p_norm.count()) == counts.loc[0, "count_clean"] == 2
assert abs(df["credit_limit"].mean() - counts.loc[0, "avg_limit"]) < 1e-9
assert abs(df["credit_limit"].fillna(0).mean() - counts.loc[0, "avg_limit_null_as_0"]) < 1e-9
print("asserts passed (pandas matches SQL in customer_id order)")

# read_csv default NA handling: which spellings become NaN?
tokens = ["", "NULL", "N/A", "NA", "None", "nan", "NaN", "null", "n/a", "#N/A", "<NA>", "Null", "na", "NAN", "   ", "-", "0"]
csv_text = "k,v\n" + "\n".join(f'{i},"{t}"' for i, t in enumerate(tokens))
got = pd.read_csv(io.StringIO(csv_text), dtype={"v": "str"})
isna = dict(zip(tokens, got["v"].isna()))
print("\nread_csv default: parsed as missing:", [t for t in tokens if isna[t]])
print("read_csv default: kept as text     :", [t for t in tokens if not isna[t]])
got2 = pd.read_csv(io.StringIO(csv_text), dtype={"v": "str"}, keep_default_na=False, na_values=["NULL", "N/A"])
print("keep_default_na=False, na_values=['NULL','N/A'] -> missing:", [t for t, m in zip(tokens, got2["v"].isna()) if m])
assert not isna["   "] and isna["NULL"] and isna["N/A"] and isna[""] and isna["None"] and not isna["Null"]
