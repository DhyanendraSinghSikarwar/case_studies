import sqlite3, random, tempfile, os
d=tempfile.mkdtemp(); p=d+"/t.db"
c=sqlite3.connect(p)
c.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL, code TEXT)")
rng=random.Random(11)
st=['delivered']*90+['placed']*6+['cancelled']*3+['returned']*1
c.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)",[(i,rng.randint(1,20000),rng.choice(st),'2024-%02d-%02d'%(rng.randint(1,12),rng.randint(1,28)),round(rng.uniform(5,500),2),str(rng.randint(1,5000))) for i in range(1,200001)])
c.execute("CREATE INDEX ix_st_dt ON orders(status,order_date)");c.execute("CREATE INDEX ix_code ON orders(code)");c.execute("CREATE INDEX ix_cust ON orders(customer_id)")
c.commit()
def plan(sql):
    k=sqlite3.connect(p); r=[x[3] for x in k.execute("EXPLAIN QUERY PLAN "+sql)]; k.close(); return r
for s in ["SELECT * FROM orders WHERE order_date='2024-03-05'","SELECT * FROM orders WHERE customer_id=5 OR amount>490","SELECT * FROM orders WHERE code LIKE '12%'"]: print(plan(s))
c.execute("ANALYZE");c.commit()
print(plan("SELECT * FROM orders WHERE order_date='2024-03-05'"))
c.execute("CREATE INDEX ix_amt ON orders(amount)");c.commit()
print(plan("SELECT * FROM orders WHERE customer_id=5 OR amount>490"))
print(plan("SELECT * FROM orders WHERE customer_id=5 OR amount=490"))
print(plan("SELECT * FROM orders WHERE status!='cancelled'"), plan("SELECT * FROM orders INDEXED BY ix_st_dt WHERE status!='cancelled'"))
print(plan("SELECT * FROM orders WHERE status IN ('delivered','placed','returned')"))
k=sqlite3.connect(p); k.execute("PRAGMA case_sensitive_like=ON"); print([x[3] for x in k.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE '12%'")])
c.execute("CREATE INDEX ix_code_nc ON orders(code COLLATE NOCASE)");c.commit()
print(plan("SELECT * FROM orders WHERE code LIKE '12%'"))
k=sqlite3.connect(p); k.execute("PRAGMA case_sensitive_like=ON"); print([x[3] for x in k.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE '12%' ")]);
print(plan("SELECT * FROM orders INDEXED BY ix_cust WHERE code='5'"))
