# Q2: clean messy customer names with TRIM, REPLACE, LOWER, LENGTH; same in pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO customers VALUES
 (1,'  Asha   Rao '),(2,'RAHUL sharma'),(3,''),(4,'Meena    Iyer     Nair'),
 (5,NULL),(6,char(9)||'Dev'||char(9)),(7,'   ');
""")

# one REPLACE only halves runs of spaces; the marker trick collapses any run to one space
sql_one = "REPLACE(TRIM(name), '  ', ' ')"
sql_three = "REPLACE(REPLACE(REPLACE(TRIM(name), '  ', ' '), '  ', ' '), '  ', ' ')"
sql_marker = ("REPLACE(REPLACE(REPLACE(TRIM(name), '  ', ' ' || char(1)), char(1) || ' ', ''), char(1), '')")
sql_clean = f"""
SELECT customer_id,
       name AS raw,
       LENGTH(name) AS len_before,
       {sql_marker} AS clean,
       LENGTH({sql_marker}) AS len_after,
       LOWER({sql_marker}) AS cmp_key
FROM customers
ORDER BY customer_id
"""
df_sql = pd.read_sql(sql_clean, con)
print(df_sql.assign(raw=df_sql.raw.map(repr)).to_string(index=False)); print()

print("--- why one REPLACE is not enough (customer 1 and 4) ---")
for cid in (1, 4):
    one, three, marker = con.execute(
        f"SELECT {sql_one}, {sql_three}, {sql_marker} FROM customers WHERE customer_id = ?", (cid,)).fetchone()
    print(cid, "one REPLACE:", repr(one), "| three REPLACEs:", repr(three), "| marker trick:", repr(marker))
# a run of 10 spaces: three passes leave a double space, the marker trick does not
one, three, marker = con.execute(
    "WITH t(name) AS (SELECT 'a' || '          ' || 'b') "
    f"SELECT {sql_one}, {sql_three}, {sql_marker} FROM t").fetchone()
print("10 spaces:", repr(one), repr(three), repr(marker))

print("\n--- TRIM semantics ---")
print("TRIM('abcba','ab') =", repr(con.execute("SELECT TRIM('abcba','ab')").fetchone()[0]), "(a set of characters, not a substring)")
print("TRIM('abab','ab')  =", repr(con.execute("SELECT TRIM('abab','ab')").fetchone()[0]))
print("TRIM('xabx','xab') =", repr(con.execute("SELECT TRIM('xabx','xab')").fetchone()[0]))
print("TRIM(tab+Dev+tab) length:", con.execute("SELECT LENGTH(TRIM(name)) FROM customers WHERE customer_id=6").fetchone()[0], "(tabs stay, 5 not 3)")
print("TRIM(name, space+tab) length:",
      con.execute("SELECT LENGTH(TRIM(name, ' ' || char(9) || char(10) || char(13))) FROM customers WHERE customer_id=6").fetchone()[0])
print("TRIM(NBSP+x+NBSP) length:", con.execute("SELECT LENGTH(TRIM(char(160) || 'x' || char(160)))").fetchone()[0], "(NBSP stays)")

# pandas
cust = pd.read_sql("SELECT * FROM customers ORDER BY customer_id", con)
p_clean = cust["name"].str.strip().str.replace(r"\s+", " ", regex=True)
p = pd.DataFrame({"customer_id": cust.customer_id, "clean": p_clean, "cmp_key": p_clean.str.casefold(),
                  "len_after": p_clean.str.len()})
print("\npandas dtype of name:", cust["name"].dtype, "| missing marker:", cust["name"][4])
print(p.to_string(index=False))
print("pandas strip on tab+Dev+tab:", repr(cust.loc[5, "name"].strip()), "-> pandas strips tabs and NBSP:",
      repr(pd.Series([" x \t"]).str.strip()[0]))

print("str.replace(r'\\s+', ' ') without regex=True leaves it alone (pandas 3 default regex=False):",
      repr(pd.Series(["a   b"]).str.replace(r"\s+", " ")[0]))
# SQL's TRIM(name) strips only spaces, so for customer 6 SQL keeps tabs: make SQL strip tabs too for a fair comparison
sql_fair = f"""SELECT customer_id,
  REPLACE(REPLACE(REPLACE(TRIM(REPLACE(REPLACE(name, char(9), ' '), char(10), ' ')), '  ', ' ' || char(1)), char(1) || ' ', ''), char(1), '') AS clean
FROM customers ORDER BY customer_id"""
fair = pd.read_sql(sql_fair, con)
assert fair["clean"].fillna("<NULL>").tolist() == p["clean"].fillna("<NULL>").tolist()
# customer 7 ('   ') and 3 ('') both end as '' in SQL and pandas; customer 5 stays NULL / NaN
assert pd.isna(fair.loc[4, "clean"]) and pd.isna(p.loc[4, "clean"])
assert fair.loc[6, "clean"] == "" == p.loc[6, "clean"]
print("asserts passed (compared in customer_id order; tabs mapped to spaces in the SQL first)")
