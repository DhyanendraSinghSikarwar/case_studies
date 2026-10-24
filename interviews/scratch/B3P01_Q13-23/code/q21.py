# String filtering: LIKE, IN, case-insensitive, literal underscore, NULLs, and the pandas equivalents (Q21).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@gmail.com','Pune'),
 (2,'arjun','arjun@Gmail.com','Delhi'),
 (3,'Ben','ben@work.in','Mumbai'),
 (4,'A_B Traders','ab@gmail.com','Pune'),
 (5,'Chitra',NULL,'Delhi'),
 (6,'Aman','aman@gmail.com.fake','Chennai'),
 (7,'Dev','dev@gmail.com',NULL),
 (8,'AxB Co','x@y.com','Pune');
""")
def ids(q, *a): return [r[0] for r in con.execute(q, a).fetchall()]

q_start = "SELECT customer_id FROM customers WHERE name LIKE 'A%' ORDER BY customer_id"
q_start_cs = "SELECT customer_id FROM customers WHERE name GLOB 'A*' ORDER BY customer_id"
q_end = "SELECT customer_id FROM customers WHERE email LIKE '%@gmail.com' ORDER BY customer_id"
q_in = "SELECT customer_id FROM customers WHERE city IN ('Pune','Delhi') ORDER BY customer_id"
q_ci = "SELECT customer_id FROM customers WHERE LOWER(email) LIKE '%@gmail.com' ORDER BY customer_id"
q_nocase = "SELECT customer_id FROM customers WHERE email COLLATE NOCASE LIKE '%@gmail.com' ORDER BY customer_id"
q_under = "SELECT customer_id FROM customers WHERE name LIKE '%\\_%' ESCAPE '\\' ORDER BY customer_id"
q_under_wrong = "SELECT customer_id FROM customers WHERE name LIKE 'A_B%' ORDER BY customer_id"

print("name LIKE 'A%' (SQLite LIKE ignores ASCII case):", ids(q_start))
print("name GLOB 'A*' (case-sensitive, SQLite only):", ids(q_start_cs))
print("email LIKE '%@gmail.com' (NULL email excluded, 'Gmail' matches):", ids(q_end))
print("city IN list:", ids(q_in), "(NULL city never matches IN)")
print("LOWER(email) LIKE ...:", ids(q_ci))
print("COLLATE NOCASE LIKE:", ids(q_nocase))
print("literal underscore with ESCAPE:", ids(q_under))
print("unescaped 'A_B%' (underscore is a wildcard for one character, so 'AxB Co' matches too):", ids(q_under_wrong))
print("PRAGMA case_sensitive_like makes LIKE case-sensitive:")
con.execute("PRAGMA case_sensitive_like = ON")
print("  name LIKE 'A%' now:", ids(q_start))
con.execute("PRAGMA case_sensitive_like = OFF")

# pandas
df = pd.read_sql("SELECT * FROM customers", con)
def pid(mask): return df.loc[mask, "customer_id"].tolist()
p_start_ci = pid(df["name"].str.lower().str.startswith("a", na=False))
p_start_cs = pid(df["name"].str.startswith("A", na=False))
p_end_ci = pid(df["email"].str.lower().str.endswith("@gmail.com", na=False))
p_in = pid(df["city"].isin(["Pune", "Delhi"]))
p_contains = pid(df["email"].str.contains("@GMAIL.COM", case=False, regex=False, na=False))
p_under = pid(df["name"].str.contains("_", regex=False, na=False))
print("pandas startswith 'A' case-sensitive:", p_start_cs, "| lower().startswith('a'):", p_start_ci)
print("pandas email endswith (lowercased):", p_end_ci, "| contains('@GMAIL.COM', case=False, regex=False):", p_contains)
print("raw str.startswith without na= on a NaN row ->", df["email"].str.startswith("a").tolist())
print("raw str.contains('gmail') with na default ->", df["email"].str.contains("gmail", regex=False).tolist())

assert ids(q_start) == p_start_ci and ids(q_start_cs) == p_start_cs
assert ids(q_ci) == ids(q_nocase) == p_end_ci
assert ids(q_end) == p_end_ci
assert ids(q_in) == p_in and ids(q_under) == p_under == [4]
assert ids(q_under_wrong) == [4, 8]
print("asserts passed (results compared as customer_id lists, ascending)")
