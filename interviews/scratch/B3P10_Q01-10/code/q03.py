# Q3: username, domain, top-level part of emails; invalid bucket; pandas split/extract.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE contacts(name TEXT, email TEXT, phone TEXT);
INSERT INTO contacts VALUES
 ('Asha',  'Asha.Rao@Example.com', '98765 43210'),
 ('Ben',   'ben@mail.example.co.in', NULL),
 ('Chitra', NULL, NULL),
 ('Dev',   '', NULL),
 ('Esha',  'esha.example.com', NULL),
 ('Farid', 'a@b@c.com', NULL),
 ('Gita',  '  gita@EXAMPLE.com  ', NULL),
 ('Hari',  'hari@example.com', NULL);
""")

sql_parse = """
WITH c AS (
  SELECT name, LOWER(TRIM(email)) AS e FROM contacts
), v AS (
  SELECT name, e,
         (e LIKE '%_@_%._%' AND LENGTH(e) - LENGTH(REPLACE(e, '@', '')) = 1) AS ok
  FROM c
), p AS (
  SELECT name, e, ok,
         CASE WHEN ok THEN SUBSTR(e, INSTR(e, '@') + 1) END AS domain
  FROM v
)
SELECT name,
       CASE WHEN ok THEN SUBSTR(e, 1, INSTR(e, '@') - 1) END AS username,
       domain,
       CASE WHEN ok THEN SUBSTR(domain, LENGTH(RTRIM(domain, REPLACE(domain, '.', ''))) + 1) END AS tld
FROM p
ORDER BY name
"""
sql_count = """
WITH c AS (SELECT LOWER(TRIM(email)) AS e FROM contacts), v AS (
  SELECT e, (e LIKE '%_@_%._%' AND LENGTH(e) - LENGTH(REPLACE(e, '@', '')) = 1) AS ok FROM c)
SELECT CASE WHEN ok THEN SUBSTR(e, INSTR(e, '@') + 1) ELSE 'invalid' END AS domain, COUNT(*) AS n
FROM v
GROUP BY 1
ORDER BY n DESC, domain
"""
# the other technique: a recursive CTE that peels one label at a time (same answer, longer)
sql_tld_cte = """
WITH RECURSIVE t(name, rest) AS (
  SELECT name, SUBSTR(LOWER(TRIM(email)), INSTR(LOWER(TRIM(email)), '@') + 1)
  FROM contacts WHERE LOWER(TRIM(email)) LIKE '%_@_%._%'
  UNION ALL
  SELECT name, SUBSTR(rest, INSTR(rest, '.') + 1) FROM t WHERE INSTR(rest, '.') > 0
)
SELECT name, rest AS tld FROM t WHERE INSTR(rest, '.') = 0 ORDER BY name
"""
parsed = pd.read_sql(sql_parse, con)
print(parsed.to_string(index=False)); print()
counts = pd.read_sql(sql_count, con)
print(counts.to_string(index=False)); print()
cte = pd.read_sql(sql_tld_cte, con)
# a@b@c.com passes the LIKE check, so the CTE returns 'com' for Farid where the guarded query returns NULL
print("recursive CTE tld (no two-@ guard):", dict(zip(cte.name, cte.tld)))
no_at = con.execute("SELECT SUBSTR(email, 1, INSTR(email, '@') - 1), SUBSTR(email, INSTR(email, '@') + 1) "
                    "FROM contacts WHERE name = 'Esha'").fetchone()
print("unguarded username and domain for 'esha.example.com' (no @, INSTR = 0):", no_at)

# pandas
df = pd.read_sql("SELECT name, email FROM contacts", con)
e = df["email"].str.strip().str.lower()
ok = e.str.fullmatch(r".+@.+\..+").fillna(False) & (e.str.count("@") == 1)
parts = e.str.extract(r"^([^@]+)@([^@]+)$")           # str.extract: columns 0 and 1
split = e.str.split("@", expand=True)                  # str.split: also works for the two-part rows
p = pd.DataFrame({"name": df.name,
                  "username": parts[0].where(ok),
                  "domain": parts[1].where(ok)})
p["tld"] = p["domain"].str.rsplit(".", n=1).str[-1]
print("\nstr.split(expand=True) column count:", split.shape[1], "(3 because 'a@b@c.com' has two @)")
print(p.to_string(index=False))
p_counts = p["domain"].fillna("invalid").value_counts().rename_axis("domain").reset_index(name="n")
p_counts = p_counts.sort_values(["n", "domain"], ascending=[False, True]).reset_index(drop=True)

pd.testing.assert_frame_equal(parsed.sort_values("name").reset_index(drop=True),
                              p.sort_values("name").reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(counts, p_counts, check_dtype=False)
print("asserts passed (parse compared after sorting by name; counts sorted by n desc, domain)")
