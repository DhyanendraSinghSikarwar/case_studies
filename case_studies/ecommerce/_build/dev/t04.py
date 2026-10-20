import sys, time; sys.path.insert(0, "_build/dev"); sys.path.insert(0, "data")
import pandas as pd, numpy as np, generate_cs04 as g, sim04 as s
o, st, cl, rd = g.generate()
o = o.drop_duplicates(["day","t_min","store","cust_x_km"]); o = o[o.cust_x_km.between(0,9)]; o.loc[o._pack_min<=0,"_pack_min"]=4.5
sxy = st[["x_km","y_km"]].values
for name, kw in [("nearest",dict(mode="nearest")),("global",dict()),("global+jit",dict(jit=True)),("global+batch",dict(batch=True)),("full",dict(jit=True,batch=True))]:
    t0=time.time(); res=[]
    for d in (0,1,2):
        out = s.simulate(o[o.day==d].reset_index(drop=True), rd[rd.day==d].reset_index(drop=True), sxy, **kw); res.append(s.summarise(out))
    print(name, f"{(time.time()-t0)/3:.1f}s", pd.DataFrame(res).mean().round(2).to_dict())
