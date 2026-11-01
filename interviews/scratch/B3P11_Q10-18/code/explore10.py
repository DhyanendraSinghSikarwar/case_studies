import sqlite3, random
rng=random.Random(11)
con=sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL, code TEXT)")
st=['delivered']*90+['placed']*6+['cancelled']*3+['returned']*1
rows=[]
for i in range(1,200001):
    rows.append((i,rng.randint(1,20000),rng.choice(st),'2024-%02d-%02d'%(rng.randint(1,12),rng.randint(1,28)),round(rng.uniform(5,500),2),str(rng.randint(1,5000))))
con.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)",rows)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
con.execute("CREATE INDEX ix_st_dt ON orders(status,order_date)")
con.execute("CREATE INDEX ix_code ON orders(code)")
con.execute("CREATE INDEX ix_part ON orders(customer_id) WHERE status='cancelled'")
n=0
def plan(sql,p=()):
    global n; n+=1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN "+sql+" "*n,p)]
for s in ["SELECT * FROM orders WHERE customer_id+0=5","SELECT * FROM orders WHERE code LIKE '%7'","SELECT * FROM orders WHERE order_date>'2024-06-01'",
 "SELECT * FROM orders WHERE status='cancelled' OR customer_id=5","SELECT * FROM orders WHERE status!='delivered'","SELECT * FROM orders WHERE status<>'delivered' AND order_date='2024-03-05'",
 "SELECT * FROM orders WHERE customer_id=5 AND status='cancelled'","SELECT * FROM orders WHERE status='delivered'","SELECT * FROM orders WHERE status='delivered' AND order_date>'2024-06-01'","SELECT * FROM orders WHERE status='placed' OR customer_id=5"]:
    print(s,plan(s))
con.execute("ANALYZE")
print(con.execute("select * from sqlite_stat1").fetchall())
for s in ["SELECT * FROM orders WHERE status!='delivered'","SELECT * FROM orders WHERE status='delivered'","SELECT * FROM orders WHERE customer_id=5 AND status='cancelled'","SELECT * FROM orders WHERE customer_id=5","SELECT * FROM orders WHERE status='cancelled' AND customer_id=5 AND order_date>'2024-01-01'"]:
    print(s,plan(s))
