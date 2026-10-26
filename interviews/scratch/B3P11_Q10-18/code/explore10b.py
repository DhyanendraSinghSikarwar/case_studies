import sqlite3, random
rng=random.Random(5)
con=sqlite3.connect(":memory:")
con.execute("CREATE TABLE w(id INTEGER PRIMARY KEY, a INT, b INT)")
con.execute("CREATE INDEX ix_a ON w(a)"); con.execute("CREATE INDEX ix_b ON w(b)")
con.executemany("INSERT INTO w(a,b) VALUES(?,?)",[(i%2,7) for i in range(1000)])
con.execute("ANALYZE"); print(con.execute("select * from sqlite_stat1").fetchall())
n=0
def plan(sql):
    global n;n+=1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN "+sql+" "*n)]
q="SELECT * FROM w WHERE a=1 AND b=500"
print(plan(q))
con.executemany("INSERT INTO w(a,b) VALUES(?,?)",[(rng.randint(0,1),rng.randint(1,100000)) for i in range(200000)])
print(plan(q))
print(con.execute("select * from sqlite_stat1").fetchall())
con.execute("ANALYZE"); print(con.execute("select * from sqlite_stat1").fetchall()); print(plan(q))
print(plan("SELECT * FROM w WHERE b=500 AND a=1"), plan("SELECT * FROM w WHERE a=1 AND b=500 AND id>0"))
con.execute("INSERT INTO w(a,b) VALUES(1,500)")
print(plan("SELECT id,a,b FROM w WHERE a=1 AND b=500"))
print(plan("SELECT * FROM w WHERE b=500"))
