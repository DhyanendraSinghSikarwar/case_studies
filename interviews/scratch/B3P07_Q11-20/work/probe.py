import sqlite3, pandas as pd, numpy as np, itertools, datetime as dt
print(sqlite3.sqlite_version, pd.__version__)
con=sqlite3.connect(":memory:")
# julianday precision at exact 30 min
bad=0;tot=0;worst=0
base=dt.datetime(2024,1,1)
rows=[]
for i in range(0,20000):
    a=base+dt.timedelta(minutes=7*i+3,seconds=i%60)
    b=a+dt.timedelta(minutes=30)
    rows.append((a.strftime('%Y-%m-%d %H:%M:%S'),b.strftime('%Y-%m-%d %H:%M:%S')))
con.execute("create table t(a,b)");con.executemany("insert into t values(?,?)",rows)
print(con.execute("select count(*), sum((julianday(b)-julianday(a))*1440 > 30), sum((julianday(b)-julianday(a))*1440 < 30), sum((julianday(b)-julianday(a))*1440 = 30), sum(unixepoch(b)-unixepoch(a) = 1800) from t").fetchone())
print(con.execute("select (julianday(b)-julianday(a))*1440 from t where (julianday(b)-julianday(a))*1440 > 30 limit 3").fetchall())
print(con.execute("select a,b,(julianday(b)-julianday(a))*1440 from t where (julianday(b)-julianday(a))*1440 <> 30 limit 2").fetchall())
# MAX frame
print(con.execute("select x, max(x) over (order by x rows between unbounded preceding and 1 preceding) from (select 3 x union all select 1 union all select 5 union all select 2) ").fetchall())
# pandas probes
s=pd.Series(['a',None,None,'b']); print((s!=s.shift()).tolist(), (np.nan!=np.nan))
print(pd.Series([1,2,3]).shift().dtype, pd.Series([1,2,3]).shift(fill_value=0).dtype)
d=pd.DataFrame({'k':[1,1,np.nan,np.nan],'v':[1,2,3,4]});print(d.groupby('k').v.sum().to_dict(), d.groupby('k',dropna=False).v.sum().to_dict())
print(pd.Series([3,1,2,5,4]).rolling(3).min().tolist(), pd.Series([3,1,2,5,4]).rolling(3,min_periods=1).min().tolist())
# sort stability single key
n=2000; df=pd.DataFrame({'k':np.random.RandomState(0).randint(0,3,n),'o':range(n)})
r=df.sort_values('k'); print("single-key default stable?", all(r.groupby('k').o.apply(lambda x:x.is_monotonic_increasing)))
r=df.sort_values('k',kind='stable'); print("stable kind", all(r.groupby('k').o.apply(lambda x:x.is_monotonic_increasing)))
df['k2']=0; r=df.sort_values(['k','k2']); print("multi-key stable?", all(r.groupby('k').o.apply(lambda x:x.is_monotonic_increasing)))
# cummax dt
g=pd.DataFrame({'r':[1,1,1,2],'e':pd.to_datetime(['2024-01-05','2024-01-03',None,'2024-01-01'])})
print(g.groupby('r').e.cummax().tolist())
print(g.groupby('r').e.cummax().groupby(g.r).shift().tolist())
# concat tie order
a=pd.DataFrame({'t':[1,1],'s':['a1','a2']});b=pd.DataFrame({'t':[1],'s':['b1']})
print(pd.concat([a,b]).sort_values('t').s.tolist(), pd.concat([a,b]).sort_values('t',kind='stable').s.tolist())
print([ (k,len(list(g))) for k,g in itertools.groupby(['ok','ok','down','ok'])])
