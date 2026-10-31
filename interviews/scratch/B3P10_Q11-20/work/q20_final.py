# Q20: phone numbers without regular expressions (SQLite) versus pandas str.replace(r'\D')
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts(id INTEGER PRIMARY KEY, name TEXT, phone TEXT);
INSERT INTO contacts VALUES
 (1,'Asha','+91 98765-43210'),
 (2,'Ben','(022) 2345 6789'),
 (3,'Chitra','098765 43210'),
 (4,'Dev','9876543210'),
 (5,'Esha','98765 43210 ext 12'),
 (6,'Farid',NULL),
 (7,'Gita','98765-4321');
""")
print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)

SQL_PHONE = """
WITH c AS (
  SELECT id, name, phone,
         REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(phone, ' ', ''), '-', ''), '(', ''), ')', ''), '+', '') AS d
  FROM contacts
), s AS (
  SELECT *,
         CASE WHEN phone IS NULL THEN 'missing'
              WHEN d GLOB '*[^0-9]*' THEN 'review: non-digit (extension or text)'
              WHEN (LENGTH(d) = 10 AND d GLOB '[6-9]*')
                OR (LENGTH(d) = 11 AND d GLOB '0[6-9]*')
                OR (LENGTH(d) = 12 AND d GLOB '91[6-9]*') THEN 'ok'
              WHEN LENGTH(d) = 11 AND d GLOB '0*' THEN 'review: landline with STD code'
              ELSE 'review: length ' || LENGTH(d)
         END AS status
  FROM c
)
SELECT id, name, phone, d AS cleaned, status,
       CASE WHEN status = 'ok'
            THEN PRINTF('+91-%s-%s', SUBSTR(d, -10, 5), SUBSTR(d, -5))
       END AS standard
FROM s ORDER BY id
"""
sql = pd.read_sql_query(SQL_PHONE, con)
print("\nSQL:"); print(sql.to_string(index=False))

contacts = pd.read_sql_query("SELECT * FROM contacts ORDER BY id", con)
d = contacts["phone"].str.replace(r"[ \-()+]", "", regex=True)           # same cleaning as the nested REPLACE
has_other = d.str.contains(r"[^0-9]", regex=True)                          # letters etc. (check BEFORE removing them)
n = d.str.len()
ok = ((n == 10) & d.str.match(r"[6-9]")) | ((n == 11) & d.str.match(r"0[6-9]")) | ((n == 12) & d.str.match(r"91[6-9]"))
status = np.select(
    [contacts["phone"].isna(), has_other.fillna(False), ok.fillna(False), (n == 11) & d.str.match(r"0"),],
    ["missing", "review: non-digit (extension or text)", "ok", "review: landline with STD code"],
    default="review: length " + n.astype("Int64").astype(str))
last10 = d.str[-10:]
standard = np.where(status == "ok", "+91-" + last10.str[:5] + "-" + last10.str[5:], None)
p = pd.DataFrame({"id": contacts["id"], "cleaned": d, "status": status, "standard": standard})
print("\npandas:"); print(p.to_string(index=False))

# comparison: ordered by id; NULL equals NaN/None
s_cmp = sql[["id", "cleaned", "status", "standard"]].copy()
for col in ("cleaned", "standard"):
    s_cmp[col] = s_cmp[col].astype(object).where(s_cmp[col].notna(), None)
    p[col] = p[col].astype(object).where(p[col].notna(), None)
assert s_cmp["status"].tolist() == p["status"].tolist()
assert s_cmp["standard"].tolist() == p["standard"].tolist()
assert s_cmp["cleaned"].tolist() == p["cleaned"].tolist()
print("\nasserts passed (status, cleaned digits and standard form equal, ordered by id)")

# the trap: strip everything that is not a digit first, then take the last 10
naive = contacts["phone"].str.replace(r"\D", "", regex=True).str[-10:]
print("\nnaive pandas str.replace(r'\\D', '').str[-10:]:")
print(pd.DataFrame({"phone": contacts["phone"], "naive_last10": naive}).to_string(index=False))
assert naive[4] == "7654321012" and naive[1] == "2223456789" and naive[2] == "9876543210"
print("row 5 (extension) and row 2 (landline) silently become 10-digit 'numbers'; the status check above refuses them")
print("SQLite SUBSTR(x, -10) on a 5-char string:", con.execute("SELECT SUBSTR('12345', -10)").fetchone()[0], "(returns what exists, no error)")
