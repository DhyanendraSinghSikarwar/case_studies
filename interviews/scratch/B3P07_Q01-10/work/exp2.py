import sqlite3, random
con=sqlite3.connect(":memory:")
random.seed(1)
bad=0;tot=0
for t in range(3000):
    h,m,s,ms=random.randint(0,23),random.randint(0,59),random.randint(0,59),random.randint(0,999)
    y=random.choice([2020,2024,2026]); mo=random.randint(1,12); d=random.randint(1,25)
    keys=set()
    for i in range(3):
        ts=con.execute("select strftime('%Y-%m-%d %H:%M:%f',?,?)",(f"{y}-{mo:02d}-{d:02d} {h:02d}:{m:02d}:{s:02d}.{ms:03d}",f"+{i} day")).fetchone()[0]
        keys.add(con.execute("select julianday(?)-?",(ts,i+1)).fetchone()[0])
    tot+=1;bad+=len(keys)>1
print(bad,tot)
print(con.execute("select julianday('2024-03-01 10:00:00.123')-julianday('2024-02-29 10:00:00.123')").fetchone())
