import sqlite3, itertools
import pandas as pd, numpy as np
con=sqlite3.connect(":memory:")
print(con.execute("select julianday('2024-03-01'), julianday('2024-03-01')-1, julianday('2024-02-29')").fetchall())
# float precision with timestamps: consecutive days same time-of-day, key = jd - rn
bad=0;tot=0
import datetime
base=datetime.datetime(2024,1,1,13,17,41)
for off in range(0,4000,7):
    for n in (5,):
        keys=set()
        for i in range(n):
            ts=(base+datetime.timedelta(days=off+i,seconds=0)).strftime('%Y-%m-%d %H:%M:%S')
            k=con.execute("select julianday(?)-?",(ts,i+1)).fetchone()[0]
            keys.add(k)
        tot+=1; bad+= len(keys)>1
print("julianday ts keys split:",bad,"of",tot)
bad=0
for off in range(0,4000,7):
    keys=set()
    for i in range(5):
        ts=(base+datetime.timedelta(days=off+i)).strftime('%Y-%m-%d %H:%M:%S')
        keys.add(con.execute("select unixepoch(?)-86400*?",(ts,i+1)).fetchone()[0])
    bad+=len(keys)>1
print("unixepoch split:",bad)
print(con.execute("select typeof(julianday('2024-03-01')), typeof(unixepoch('2024-03-01')), unixepoch('2024-03-01'), unixepoch('2024-03-01')/86400, CAST(julianday('2024-03-01') AS INTEGER), julianday('2024-03-01')+0.5").fetchall())
print(con.execute("select '2024-03-01'-1, '2024-12-31'+0, '2025-01-01'+0").fetchall())
# pandas facts
s=pd.Series(["up","up",None,"down"])
print((s!=s.shift()).tolist())
print(pd.Series([1.0,np.nan])!=pd.Series([1.0,np.nan]))
print(pd.Series([1,2,3]).shift().dtype, pd.Series([1,2,3]).shift(fill_value=0).dtype)
df=pd.DataFrame({"k":[1,None,1,None],"v":[1,2,3,4]})
print(df.groupby("k")["v"].sum().to_dict(), df.groupby("k",dropna=False)["v"].sum().to_dict())
d=pd.DataFrame({"a":[2,1,2,1,2],"b":range(5)})
print(d.sort_values("a").b.tolist(), d.sort_values("a",kind="quicksort").b.tolist())
print([(k,len(list(g))) for k,g in itertools.groupby(["up","up","down","down","down","up"])])
