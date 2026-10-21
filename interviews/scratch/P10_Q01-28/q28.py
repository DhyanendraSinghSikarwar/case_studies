import numpy as np, pandas as pd, statsmodels.formula.api as smf
rng=np.random.default_rng(0)
rows=[]
for city in range(40):
    treated=city<20; base=rng.normal(100,5)
    for t in range(12):
        post=t>=6
        y=base+2*t+(5 if treated and post else 0)+rng.normal(0,2)  # common trend 2/period, true effect 5
        rows.append((city,treated*1,post*1,t,y))
df=pd.DataFrame(rows,columns=["city","treated","post","t","y"])
m=smf.ols("y~treated*post",df).fit(cov_type="cluster",cov_kwds={"groups":df.city})
print(m.params["treated:post"].round(2), m.bse["treated:post"].round(2))
# pre-trend check
pre=df[df.post==0]; m2=smf.ols("y~treated*t",pre).fit(cov_type="cluster",cov_kwds={"groups":pre.city})
print("pre-trend diff slope", m2.params["treated:t"].round(3), "p", m2.pvalues["treated:t"].round(2))
