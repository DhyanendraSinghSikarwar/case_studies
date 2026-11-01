# Duplicates that differ only by case, spaces and NBSP: normalised key, groups, keeper, flag.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT)")
con.executemany("INSERT INTO customers VALUES (?,?,?,?)", [
    (1, "Asha Rao ", "a@x.com", "Pune"),
    (2, "asha  rao", " a@x.com", "pune"),
    (3, "Asha Rao", "A@X.com", "Pune "),
    (4, "Ben Cruz", "ben@y.com", "Delhi"),
    (5, "Ben Cruz", "ben2@y.com", "Mumbai"),      # same name, different city: not a duplicate
    (6, "Chitra Nair", "c@z.com", "Goa"),
    (7, "chitra nair", None, "GOA"),              # duplicate by name and city, email missing
    (8, "Raj Shah", "raj1@q.com", "Pune"),        # two real people with the same name and city
    (9, "Raj Shah", "raj2@q.com", "Pune"),
    (10, "Dev Rao", None, "Pune"),
])

# normalised key as a reusable CTE: NBSP and tab to space, collapse spaces, trim, ASCII lower
NORM = lambda col: (f"lower(trim(replace(replace(replace(replace(replace({col}, char(160), ' '), char(9), ' '),"
                    f" '  ', ' '), '  ', ' '), '  ', ' ')))")
groups_sql = f"""
WITH k AS (
  SELECT customer_id, name, email, city,
         {NORM('name')} AS name_key, {NORM('city')} AS city_key,
         lower(trim(replace(email, char(160), ''))) AS email_key
  FROM customers
)
SELECT name_key, city_key,
       COUNT(*)                                              AS n,
       group_concat(customer_id, ',' ORDER BY customer_id)   AS ids,
       MIN(customer_id)                                      AS keep_id,
       COUNT(DISTINCT email_key)                             AS distinct_emails,
       SUM(email_key IS NULL)                                AS null_emails
FROM k GROUP BY name_key, city_key HAVING COUNT(*) > 1
ORDER BY MIN(customer_id)"""
sql_groups = pd.read_sql(groups_sql, con)
print(sql_groups.to_string(index=False))

# flag instead of delete: dup_of points at the smallest id of the group
con.execute("ALTER TABLE customers ADD COLUMN dup_of INTEGER")
flag_sql = f"""
UPDATE customers SET dup_of = (
  SELECT MIN(c2.customer_id) FROM customers c2
  WHERE {NORM('c2.name')} = {NORM('customers.name')} AND {NORM('c2.city')} = {NORM('customers.city')})
WHERE customer_id <> (
  SELECT MIN(c2.customer_id) FROM customers c2
  WHERE {NORM('c2.name')} = {NORM('customers.name')} AND {NORM('c2.city')} = {NORM('customers.city')})"""
con.execute(flag_sql)
print("flagged:", con.execute("SELECT customer_id, dup_of FROM customers WHERE dup_of IS NOT NULL ORDER BY 1").fetchall())
# review step before any delete: show the groups where emails disagree
print("needs review (two different non-null emails):",
      [tuple(r) for r in sql_groups.loc[sql_groups["distinct_emails"] > 1, ["name_key", "city_key", "ids"]].itertuples(index=False)])
print("rows that a DELETE WHERE dup_of IS NOT NULL would remove:", con.execute("SELECT COUNT(*) FROM customers WHERE dup_of IS NOT NULL").fetchone()[0])

# ---- pandas
df = pd.read_sql("SELECT customer_id, name, email, city FROM customers", con)
def norm(s):
    return (s.str.replace(" ", " ", regex=False).str.replace(r"\s+", " ", regex=True)
             .str.strip().str.casefold())
df["name_key"], df["city_key"] = norm(df["name"]), norm(df["city"])
df["email_key"] = df["email"].str.replace(" ", "", regex=False).str.strip().str.casefold()
dup_mask = df.duplicated(subset=["name_key", "city_key"], keep=False)
p_groups = (df[dup_mask].groupby(["name_key", "city_key"])
              .agg(n=("customer_id", "size"), ids=("customer_id", lambda s: ",".join(map(str, sorted(s)))),
                   keep_id=("customer_id", "min"), distinct_emails=("email_key", "nunique"),
                   null_emails=("email_key", lambda s: int(s.isna().sum())))
              .reset_index().sort_values("keep_id").reset_index(drop=True))
print(p_groups.to_string(index=False))
pd.testing.assert_frame_equal(p_groups, sql_groups, check_dtype=False)     # compared in keep_id order

kept = df.sort_values("customer_id").drop_duplicates(subset=["name_key", "city_key"], keep="first")
removed = sorted(set(df["customer_id"]) - set(kept["customer_id"]))
assert removed == sorted(r[0] for r in con.execute("SELECT customer_id FROM customers WHERE dup_of IS NOT NULL"))
print("pandas would drop ids:", removed, "| duplicated(keep=False) rows:", int(dup_mask.sum()))

# why the careless key fails
naive = con.execute("SELECT COUNT(*) FROM (SELECT name, city FROM customers GROUP BY name, city HAVING COUNT(*) > 1)").fetchone()[0]
print("exact GROUP BY name, city finds", naive, "duplicate groups; the normalised key finds", len(sql_groups))
print("ASCII-only warning:", con.execute("SELECT lower('RENÉ') = lower('rené')").fetchone()[0], "(0: É not folded by SQLite lower)")
con.close()
print("asserts passed")
