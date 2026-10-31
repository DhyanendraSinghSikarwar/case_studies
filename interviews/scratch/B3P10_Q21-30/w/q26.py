# Q26: NULLs in UNIQUE, CHECK, non-INTEGER PRIMARY KEY and tri-state flags; pandas nullable boolean.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE u_unique(email TEXT UNIQUE);
CREATE TABLE u_check(age INTEGER CHECK(age >= 18));
CREATE TABLE u_pk(code TEXT PRIMARY KEY, n INTEGER);
CREATE TABLE u_pk_nn(code TEXT PRIMARY KEY NOT NULL, n INTEGER);
CREATE TABLE u_pk_wr(code TEXT PRIMARY KEY, n INTEGER) WITHOUT ROWID;
CREATE TABLE u_pk_int(id INTEGER PRIMARY KEY, n INTEGER);
""")
def attempt(label, sql):
    try:
        con.execute(sql); print(f"  ok   : {label}")
    except sqlite3.Error as e:
        print(f"  FAIL : {label} -> {e}")
attempt("UNIQUE email, first NULL", "INSERT INTO u_unique VALUES (NULL)")
attempt("UNIQUE email, second NULL", "INSERT INTO u_unique VALUES (NULL)")
attempt("UNIQUE email, 'a' twice (second)", "INSERT INTO u_unique VALUES ('a')"); attempt("   ... duplicate 'a'", "INSERT INTO u_unique VALUES ('a')")
attempt("CHECK age=17", "INSERT INTO u_check VALUES (17)")
attempt("CHECK age=NULL", "INSERT INTO u_check VALUES (NULL)")
attempt("CHECK age=18", "INSERT INTO u_check VALUES (18)")
attempt("TEXT PRIMARY KEY NULL (1)", "INSERT INTO u_pk VALUES (NULL, 1)")
attempt("TEXT PRIMARY KEY NULL (2)", "INSERT INTO u_pk VALUES (NULL, 2)")
attempt("TEXT PRIMARY KEY NOT NULL, NULL", "INSERT INTO u_pk_nn VALUES (NULL, 1)")
attempt("WITHOUT ROWID PK, NULL", "INSERT INTO u_pk_wr VALUES (NULL, 1)")
attempt("INTEGER PRIMARY KEY, NULL", "INSERT INTO u_pk_int VALUES (NULL, 1)")
print("INTEGER PRIMARY KEY got id:", con.execute("SELECT id FROM u_pk_int").fetchone()[0],
      "| NULL rows in u_unique:", con.execute("SELECT COUNT(*) FROM u_unique WHERE email IS NULL").fetchone()[0],
      "| NULL rows in u_pk:", con.execute("SELECT COUNT(*) FROM u_pk WHERE code IS NULL").fetchone()[0])

# allow at most one NULL: a partial unique index on a constant for the NULL rows
con.executescript("CREATE TABLE u_one(email TEXT); CREATE UNIQUE INDEX u_one_null ON u_one((email IS NULL)) WHERE email IS NULL;")
attempt("u_one NULL (1)", "INSERT INTO u_one VALUES (NULL)")
attempt("u_one NULL (2)", "INSERT INTO u_one VALUES (NULL)")
attempt("u_one 'a' then 'a' again", "INSERT INTO u_one VALUES ('a'),('a')")

con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_active INTEGER);          -- 1, 0 or NULL
INSERT INTO users VALUES (1,1),(2,1),(3,0),(4,NULL),(5,NULL);
""")
sql_probe = """
SELECT user_id, is_active,
       is_active = 0        AS eq0,
       NOT is_active        AS not_flag,
       is_active IS TRUE    AS is_true,
       is_active IS FALSE   AS is_false,
       is_active IS NOT TRUE AS is_not_true,
       is_active IS NULL    AS is_null
FROM users ORDER BY user_id"""
print(pd.read_sql(sql_probe, con).to_string(index=False))
sql_counts = """
SELECT SUM(is_active IS TRUE) AS active, SUM(is_active IS FALSE) AS inactive, SUM(is_active IS NULL) AS unknown, COUNT(*) AS total
FROM users"""
sql_row = con.execute(sql_counts).fetchone()
print("counts (active, inactive, unknown, total):", sql_row)
print("WHERE is_active = 0 :", [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active = 0")])
print("WHERE is_active <> 1:", [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active <> 1")])
print("WHERE is_active IS NOT TRUE:", [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active IS NOT TRUE ORDER BY user_id")])
print("NULL IS TRUE / NULL IS NOT TRUE / NOT NULL:", con.execute("SELECT NULL IS TRUE, NULL IS NOT TRUE, NOT NULL").fetchone())

# pandas
u = pd.read_sql("SELECT * FROM users ORDER BY user_id", con)
print("read_sql dtype of is_active:", u["is_active"].dtype, "(NULL made it float64 with NaN)")
print("float: == 0 ->", u.index[u["is_active"] == 0].tolist(), "| != 1 ->", u.index[u["is_active"] != 1].tolist(), "(NaN != 1 is True in pandas, unlike SQL)")
flag = u["is_active"].astype("boolean")                      # nullable boolean: True, False, <NA>
print("boolean dtype:", flag.tolist())
print("== False ->", (flag == False).tolist(), "| ~flag ->", (~flag).tolist())     # noqa: E712
try:
    bool(flag.iloc[3])
except TypeError as e:
    print("bool(pd.NA):", e)
print("df[flag == False] rows:", u[flag == False]["user_id"].tolist(), "(NA in a mask counts as False)")   # noqa: E712
p_counts = (int((flag == True).sum()), int((flag == False).sum()), int(flag.isna().sum()), len(flag))     # noqa: E712
is_not_true = (flag != True).fillna(True)                    # NA != True is NA: fill to mimic IS NOT TRUE   # noqa: E712
print("pandas counts:", p_counts, "| IS NOT TRUE ids:", u.loc[is_not_true, "user_id"].tolist())
assert tuple(sql_row) == p_counts == (2, 1, 2, 5) and sum(p_counts[:3]) == p_counts[3]
assert u.loc[is_not_true, "user_id"].tolist() == [r[0] for r in con.execute("SELECT user_id FROM users WHERE is_active IS NOT TRUE ORDER BY user_id")] == [3, 4, 5]
print("asserts passed (SQL counts and IS NOT TRUE rows == pandas, ordered by user_id)")
