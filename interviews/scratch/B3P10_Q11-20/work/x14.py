import pandas as pd, numpy as np
df = pd.DataFrame({
 "region":["East","East","East","East","West","West","West","North"],
 "product":["Pen","Pen","Pen","Book","Pen","Book",None,"Pen"],
 "month":["Jan","Jan","Feb","Jan","Feb","Mar","Jan","Jan"],
 "amount":[100,50,np.nan,200,70,30,40,np.nan]})
print(df.dtypes)
try: df.pivot(index="region",columns="month",values="amount")
except Exception as e: print(type(e).__name__, e)
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="sum"))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",dropna=False))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",fill_value=0))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc=lambda s: s.sum(min_count=1)))
print(df.pivot_table(index="product",columns="month",values="amount",aggfunc="sum"))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc=["sum","mean"]))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc={"amount":"count"}))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",margins=True,margins_name="Total"))
print(pd.crosstab(df["region"],df["month"]))
print(pd.crosstab(df["region"],df["month"],values=df["amount"],aggfunc="sum"))
c=df.assign(month=pd.Categorical(df["month"],categories=["Jan","Feb","Mar","Apr"],ordered=True))
print(c.pivot_table(index="region",columns="month",values="amount",aggfunc="sum"))
print(c.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",observed=False))
print(c.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",observed=True,dropna=False))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",dropna=False,fill_value=0))
