import sqlite3, pandas as pd, numpy as np, io
print(sqlite3.sqlite_version, pd.__version__)
c=sqlite3.connect(":memory:")
c.executescript("""create table t(a TEXT, b INTEGER, c NUMERIC, d REAL, e);
insert into t values(' 12',' 12',' 12',' 12',' 12');
insert into t values('12 ','12 ','12 ','12 ','12 ');
insert into t values('1e3','1e3','1e3','1e3','1e3');
insert into t values('0x10','0x10','0x10','0x10','0x10');
insert into t values('2.50','2.50','2.50','2.50','2.50');
insert into t values('007','007','007','007','007');""")
for r in c.execute("select typeof(a),a,typeof(b),b,typeof(c),c,typeof(d),d,typeof(e),e from t"): print(r)
c.executescript("create table s(a INTEGER, b TEXT, c ANY) STRICT;")
for q in ["insert into s values('12','x',1)","insert into s values(' 12','x',1)","insert into s values('abc','x',1)","insert into s values(1,5,'z')","insert into s values(2.5,'x',1)","insert into s values(3.0,'x',1)"]:
    try: c.execute(q); print("ok",q)
    except Exception as e: print("ERR",q,e)
print(c.execute("select a,typeof(a),b,typeof(b) from s").fetchall())
print([c.execute("select printf('%.0f',?)",(x,)).fetchone() for x in (0.5,1.5,2.5,3.5)])
print(c.execute("select printf('%,d',1234567), printf('%.2f',703.125), round(703.125,2), printf('%.2f',2.675), round(2.675,2), printf('%.2f',1.005)").fetchone())
print(c.execute("select 'a' like 'A'").fetchone()); c.execute("pragma case_sensitive_like=1"); print(c.execute("select 'a' like 'A'").fetchone())
c.execute("pragma case_sensitive_like=0")
try: print(c.execute("select group_concat(distinct 'x', ',')").fetchone())
except Exception as e: print("ERR",e)
print(pd.Series(["o'neil","mc donald","ANNA-MARIE"]).str.title().tolist())
print(pd.Series(["aaaa","abab"]).str.count("aa").tolist(), pd.Series(["aaaa"]).str.count("(?=aa)").tolist())
print(pd.read_csv(io.StringIO("a,b\nNA,1\nnull,2\nNone,3\nn/a,4\nNaN,5\n,6\n#N/A,7\nnan,8\nNULL,9\n"),dtype=str)["a"].tolist())
df=pd.DataFrame({"a":["NA","null","None","n/a","NaN","","#N/A","nan","NULL","N/A","-nan","<NA>"]})
print(pd.read_csv(io.StringIO(df.to_csv(index=False)),dtype=str).a.isna().tolist())
# stack
rng=np.random.default_rng(0); w=pd.DataFrame(rng.integers(0,9,(1000,6)).astype(float),columns=list("abcdef")); w.iloc[::7,2]=np.nan
print(w.stack(future_stack=True).shape, w.stack().shape)
try: print(w.stack(future_stack=False).shape)
except Exception as e: print("ERR",e)
try: print(w.stack(dropna=True).shape)
except Exception as e: print("ERR",e)
