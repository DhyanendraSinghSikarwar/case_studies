rng = random.Random(71)
N = 300000
countries = ["IN", "US", "UK", "DE", "SG"]
types = ["view"] * 70 + ["click"] * 29 + ["purchase"] * 1       # 'purchase' is rare (1%)
rows = [(i, rng.randint(1, 20000), rng.choice(types), rng.choice(countries),
         "2024-%02d-%02d %02d:00" % (rng.randint(1, 12), rng.randint(1, 28), rng.randint(0, 23))) for i in range(1, N + 1)]
path = WORK + "/ev.db"
c = sqlite3.connect(path)
c.execute("CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_type TEXT, country TEXT, event_time TEXT)")
c.executemany("INSERT INTO events VALUES(?,?,?,?,?)", rows)
for s in ["CREATE INDEX ix_user ON events(user_id)", "CREATE INDEX ix_type ON events(event_type)",
          "CREATE INDEX ix_country_time ON events(country, event_time)"]:
    c.execute(s)
c.commit(); c.close()
df = pd.DataFrame(rows, columns=["event_id", "user_id", "event_type", "country", "event_time"])
print("distinct user_id:", df.user_id.nunique(), "| event_type counts:", df.event_type.value_counts().to_dict())

QS = {"user_id = 5": "SELECT * FROM events WHERE user_id = 5",
      "event_type = 'purchase' (rare)": "SELECT * FROM events WHERE event_type = 'purchase'",
      "event_type = 'view' (common)": "SELECT * FROM events WHERE event_type = 'view'",
      "event_time = '2024-03-05 10:00' (2nd column only)": "SELECT * FROM events WHERE event_time = '2024-03-05 10:00'",
      "country = 'IN' AND event_type = 'purchase'": "SELECT * FROM events WHERE country = 'IN' AND event_type = 'purchase'"}
def plans(title):
    print(title)
    for k, q in QS.items():
        st, res = steps(path, q)
        print(f"  {k:<52} steps {st:>9,} rows {len(res):>6,} | {' | '.join(plan(path, q))}")
def stat1():
    cc = sqlite3.connect(path)
    r = cc.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall() if cc.execute("SELECT 1 FROM sqlite_master WHERE name='sqlite_stat1'").fetchone() else None
    cc.close(); return r
print("sqlite_stat1 before ANALYZE:", stat1())
plans("--- plans before ANALYZE ---")
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
s = dict(stat1())
print("sqlite_stat1 after ANALYZE:", s)
plans("--- plans after ANALYZE ---")

print("--- the planner's pick for country AND event_type is a heuristic, not a guarantee ---")
q = "SELECT * FROM events %s WHERE country = 'IN' AND event_type = 'purchase'"
for lab, hint in (("planner's choice", ""), ("INDEXED BY ix_type", "INDEXED BY ix_type")):
    st, res = steps(path, q % hint)
    print(f"  {lab:<20} steps {st:>9,} rows {len(res)} | {' | '.join(plan(path, q % hint))}")

print("--- selectivity by hand (rows / distinct values) ---")
for idx, cols in (("ix_user", ["user_id"]), ("ix_type", ["event_type"]), ("ix_country_time", ["country", "event_time"])):
    expect = [N]
    for k in range(1, len(cols) + 1):
        expect.append(int(np.ceil(N / df.groupby(cols[:k]).ngroups)))
    got = [int(x) for x in s[idx].split()]
    print(f"  {idx:<16} stat {s[idx]!r:<22} by hand {expect}")
    assert got == expect or all(abs(a - b) <= 1 for a, b in zip(got, expect)), (got, expect)
print("  actual rows for event_type values:", df.event_type.value_counts().to_dict(), "(stat says", s["ix_type"].split()[1], "for every value)")

print("--- statistics are a snapshot: add 100,000 rows of one new user ---")
c = sqlite3.connect(path)
c.executemany("INSERT INTO events VALUES(?,?,?,?,?)", [(N + i, 999999, "view", "IN", "2024-12-31 23:00") for i in range(1, 100001)])
c.commit(); c.close()
print("stat1 unchanged:", dict(stat1())["ix_user"], "| true rows for user 999999:", 100000)
c = sqlite3.connect(path)
c.execute("SELECT COUNT(*) FROM events WHERE user_id = 999999").fetchall()     # optimize only looks at tables this connection queried
print("PRAGMA optimize(0x03) dry run (lists the ANALYZE it would run):", c.execute("PRAGMA optimize(0x03)").fetchall())
print("PRAGMA optimize(0x02) runs it:", c.execute("PRAGMA optimize(0x02)").fetchall()); c.commit(); c.close()
print("stat1 after optimize:", dict(stat1())["ix_user"], "| sqlite_stat1 rows:", len(stat1()))
c = sqlite3.connect(path)
c.execute("PRAGMA analysis_limit = 400"); c.execute("ANALYZE"); c.commit()
print("PRAGMA analysis_limit=400 then ANALYZE ->", c.execute("PRAGMA analysis_limit").fetchone(), dict(stat1()))
c.close()

print("--- PRAGMA optimize on a table whose size changed a lot (1,000 -> 51,000 rows) ---")
p2 = WORK + "/opt.db"
c = sqlite3.connect(p2)
c.execute("CREATE TABLE a(id INTEGER PRIMARY KEY, u INT)"); c.execute("CREATE INDEX ia ON a(u)")
c.executemany("INSERT INTO a(u) VALUES(?)", [(i % 100,) for i in range(1000)]); c.execute("ANALYZE"); c.commit()
c.executemany("INSERT INTO a(u) VALUES(?)", [(i % 100,) for i in range(50000)]); c.commit(); c.close()
c = sqlite3.connect(p2)
c.execute("SELECT * FROM a WHERE u = 5").fetchall()
print("stat1 now:", c.execute("SELECT * FROM sqlite_stat1").fetchall())
print("PRAGMA optimize(0x03) says:", c.execute("PRAGMA optimize(0x03)").fetchall())
c.execute("PRAGMA optimize"); c.commit()
print("stat1 after PRAGMA optimize:", c.execute("SELECT * FROM sqlite_stat1").fetchall())
c.close()
