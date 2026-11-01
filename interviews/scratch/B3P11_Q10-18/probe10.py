import sqlite3, random
URI="file:p10?mode=memory&cache=shared"
keep=sqlite3.connect(URI,uri=True)
def fresh(): return sqlite3.connect(URI,uri=True)
def plan(sql,params=()):
    c=fresh()
    try: return [r[3] for r in c.execute("EXPLAIN QUERY PLAN "+sql,params).fetchall()]
    finally: c.close()
def steps(sql,params=()):
    c=fresh(); n=[0]
    def cb(): n[0]+=1; return 0
    c.set_progress_handler(cb,1); rows=c.execute(sql,params).fetchall(); c.set_progress_handler(None,0); c.close(); return n[0],rows
rnd=random.Random(10)
N=200000
codes=rnd.sample(range(1000000),N)
st=['delivered']*90+['shipped']*4+['placed']*3+['returned']*2+['cancelled']
rows=[]
for i in range(1,N+1):
    d=rnd.randrange(731)
    import datetime
    dt=(datetime.date(2023,1,1)+datetime.timedelta(days=d)).isoformat()
    rows.append((i,rnd.randrange(1,20001),rnd.choice(st),dt,rnd.randrange(10,1000),'K%06d'%codes[i-1]))
keep.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount INT, code TEXT)")
keep.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)",rows)
for s in ["CREATE INDEX ix_cust ON orders(customer_id)","CREATE INDEX ix_status_date ON orders(status,order_date)","CREATE INDEX ix_code ON orders(code)","CREATE INDEX ix_cancel_cust ON orders(customer_id) WHERE status='cancelled'"]: keep.execute(s)
keep.commit()
qs={
"fn":"SELECT * FROM orders WHERE lower(code)='k000123'",
"fn2":"SELECT * FROM orders WHERE customer_id+0=5",
"likew":"SELECT * FROM orders WHERE code LIKE '%123'",
"likep":"SELECT * FROM orders WHERE code LIKE 'K0001%'",
"range":"SELECT * FROM orders WHERE code >= 'K0001' AND code < 'K0002'",
"second":"SELECT * FROM orders WHERE order_date='2024-03-05'",
"second_cov":"SELECT status,order_date FROM orders WHERE order_date='2024-03-05'",
"or":"SELECT * FROM orders WHERE customer_id=5 OR amount=10",
"ne":"SELECT * FROM orders WHERE status != 'delivered'",
"in":"SELECT * FROM orders WHERE status IN ('shipped','placed','returned','cancelled')",
"ne_c":"SELECT * FROM orders WHERE status != 'cancelled'",
"part1":"SELECT * FROM orders WHERE customer_id=5",
"part2":"SELECT * FROM orders WHERE customer_id=5 AND status='cancelled'",
"part3":"SELECT * FROM orders WHERE customer_id=5 AND status IN ('cancelled')",
"part4":"SELECT customer_id FROM orders WHERE status='cancelled'",
"deliv":"SELECT * FROM orders WHERE status='delivered'",
}
for k,q in qs.items(): print(k,plan(q), steps(q)[0], len(steps(q)[1]))
print(plan("SELECT * FROM orders WHERE status='delivered'"))
print(steps("SELECT * FROM orders NOT INDEXED WHERE status='delivered'")[0], steps("SELECT * FROM orders INDEXED BY ix_status_date WHERE status='delivered'")[0])
c=keep; c.execute("ANALYZE"); c.commit()
print(c.execute("select * from sqlite_stat1").fetchall())
for k in ["second","second_cov","deliv","part2"]: print(k,plan(qs[k]),steps(qs[k])[0])
print("-----")
def tryp(q):
    try: print(q, plan(q), steps(q)[0])
    except Exception as e: print(q,"ERR",e)
tryp("SELECT * FROM orders INDEXED BY ix_cancel_cust WHERE customer_id=5")
tryp("SELECT * FROM orders INDEXED BY ix_cancel_cust WHERE customer_id=5 AND status='cancelled'")
tryp("SELECT * FROM orders INDEXED BY ix_nonexist WHERE customer_id=5")
tryp("SELECT * FROM orders INDEXED BY ix_code WHERE customer_id=5")
tryp("SELECT * FROM orders INDEXED BY ix_code WHERE code='K000001'")
tryp("SELECT * FROM orders NOT INDEXED WHERE customer_id=5")
# fixes
tryp("SELECT * FROM orders WHERE status < 'delivered' OR status > 'delivered'")
tryp("SELECT * FROM orders WHERE customer_id=5 UNION ALL SELECT * FROM orders WHERE amount=10 AND customer_id<>5")
keep.execute("CREATE INDEX ix_amount ON orders(amount)"); keep.commit()
tryp("SELECT * FROM orders WHERE customer_id=5 OR amount=10")
tryp("SELECT * FROM orders WHERE order_date='2024-03-05'")
# case_sensitive_like
c=fresh()
print(c.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE 'K0001%'").fetchall())
print(c.execute("SELECT count(*) FROM orders WHERE code LIKE 'k0001%'").fetchone())
c.execute("PRAGMA case_sensitive_like=ON")
print(c.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE 'K0001%'").fetchall())
print(c.execute("SELECT count(*) FROM orders WHERE code LIKE 'k0001%'").fetchone(), c.execute("SELECT count(*) FROM orders WHERE code LIKE 'K0001%'").fetchone())
print(c.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE 'k0001%'").fetchall())
