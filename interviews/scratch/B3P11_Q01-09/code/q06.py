# Q6: LIKE and indexes in SQLite (BINARY vs NOCASE index, prefix range, expression index, reversed string, FTS5).
import random
import sqlite3
import pandas as pd

random.seed(6)
first = ["Asha", "Rahul", "Priya", "Vikram", "Meera", "Arjun", "Kavya", "Ishaan", "Neha", "Sanjay"]
last = ["Rao", "Sharma", "Iyer", "Gupta", "Nair", "Patel", "Singh", "Menon", "Das", "Khan"]
def mk(i):
    f, l = random.choice(first), random.choice(last)
    n = f"{f} {l}"
    r = random.random()
    if r < 0.05: n = n.upper()        # upper case variant
    elif r < 0.10: n = n.lower()      # 'asha rao'
    return (i, f"user{i}@example.com", n, random.choice(["Pune", "Delhi"]))
rows = [mk(i) for i in range(1, 100001)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, email TEXT, name TEXT, city TEXT)")
con.executemany("INSERT INTO users VALUES (?,?,?,?)", rows)
con.execute("CREATE INDEX ix_email ON users(email)")
con.execute("CREATE INDEX ix_name ON users(name)")
con.commit()

_n = [0]
def plan(where):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute(f"EXPLAIN QUERY PLAN SELECT * FROM users WHERE {where}" + " " * _n[0]))
def run(where):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(f"SELECT user_id FROM users WHERE {where}").fetchall()
    con.set_progress_handler(None, 0)
    return c[0], sorted(r[0] for r in out)

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 80)
tests = ["name LIKE 'Asha%'", "name LIKE '%Rao%'", "name LIKE '%Rao'", "lower(name) = 'asha rao'",
         "name >= 'Asha' AND name < 'Ashb'", "name GLOB 'Asha*'"]
res = [(w, plan(w), run(w)[0], len(run(w)[1])) for w in tests]
print("-- plain index ix_name (BINARY collation)")
print(pd.DataFrame(res, columns=["predicate", "plan", "vm_steps", "rows"]).to_string(index=False))

# fix 1: NOCASE index
con.execute("CREATE INDEX ix_name_nc ON users(name COLLATE NOCASE)")
w = "name LIKE 'Asha%'"
print("\n-- with ix_name_nc ON users(name COLLATE NOCASE)")
print(plan(w), run(w)[0], len(run(w)[1]))
like_ids = run(w)[1]

# the prefix range gives a different (case-sensitive) answer than LIKE
rng = run("name >= 'Asha' AND name < 'Ashb'")[1]
glob = run("name GLOB 'Asha*'")[1]
print("LIKE rows:", len(like_ids), " BINARY prefix-range rows:", len(rng), " GLOB rows:", len(glob))
assert set(rng) <= set(like_ids) and rng == glob and len(like_ids) > len(rng)

# fix 2: PRAGMA case_sensitive_like = ON (changes results; use a fresh connection to see it clearly)
con2 = sqlite3.connect(":memory:")
con2.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, email TEXT, name TEXT, city TEXT)")
con2.executemany("INSERT INTO users VALUES (?,?,?,?)", rows)
con2.execute("CREATE INDEX ix_name ON users(name)")
con2.execute("PRAGMA case_sensitive_like = ON")
p = " | ".join(r[3] for r in con2.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE name LIKE 'Asha%'"))
n_on = con2.execute("SELECT COUNT(*) FROM users WHERE name LIKE 'Asha%'").fetchone()[0]
print("\ncase_sensitive_like=ON plan:", p, "| rows:", n_on, "(was", len(like_ids), "with the default)")
assert n_on == len(rng)

# expression index for lower(name)
con.execute("CREATE INDEX ix_lower ON users(lower(name))")
w = "lower(name) = 'asha rao'"
print("\nexpression index on lower(name):", plan(w), run(w)[0], len(run(w)[1]))

# suffix search: store the reversed string, index it, search with a prefix on the reversed text
con.execute("ALTER TABLE users ADD COLUMN name_rev TEXT")
con.executemany("UPDATE users SET name_rev = ? WHERE user_id = ?", [(r[2][::-1].lower(), r[0]) for r in rows])
con.execute("CREATE INDEX ix_rev ON users(name_rev)")
w = "name_rev >= 'oar' AND name_rev < 'oas'"
print("suffix 'rao' via reversed column:", plan(w), run(w)[0], len(run(w)[1]))
suffix_scan = run("lower(name) LIKE '%rao'")
assert suffix_scan[1] == run(w)[1]
print("full scan LIKE '%rao' steps:", suffix_scan[0], "rows:", len(suffix_scan[1]), "(same rows)")

# FTS5
print("\nFTS5 compiled in:", ("ENABLE_FTS5",) in con.execute("PRAGMA compile_options").fetchall())
con.execute("CREATE VIRTUAL TABLE fts USING fts5(name)")
con.executemany("INSERT INTO fts(rowid, name) VALUES (?,?)", [(r[0], r[2]) for r in rows])
print("FTS5 plan:", " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT rowid FROM fts WHERE fts MATCH 'asha'")))
fts_ids = sorted(r[0] for r in con.execute("SELECT rowid FROM fts WHERE fts MATCH 'asha'"))
print("MATCH 'asha' (whole word, case-insensitive):", len(fts_ids), "| prefix query 'ash*':",
      con.execute("SELECT COUNT(*) FROM fts WHERE fts MATCH 'ash*'").fetchone()[0])
assert fts_ids == like_ids

# pandas: str.startswith is a scan; case handling is explicit
df = pd.DataFrame(rows, columns=["user_id", "email", "name", "city"])
p_like = sorted(df[df.name.str.lower().str.startswith("asha")].user_id)
p_bin = sorted(df[df.name.str.startswith("Asha")].user_id)
assert p_like == like_ids and p_bin == rng
print("\npandas: str.lower().str.startswith('asha') =", len(p_like), "rows (= LIKE); str.startswith('Asha') =", len(p_bin), "(= BINARY range)")
