import pandas as pd, numpy as np
df = pd.DataFrame({
 "region":["East","East","East","East","West","West","West","North"],
 "product":["Pen","Pen","Pen","Book","Pen","Book",None,"Pen"],
 "month":["Jan","Jan","Feb","Jan","Feb","Mar","Jan","Jan"],
 "amount":[100,50,np.nan,200,70,30,40,np.nan]})
f=lambda s: s.sum(min_count=1)
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc=f,dropna=False))
print(df.groupby(["region","month"])["amount"].sum(min_count=1).unstack())
print(df.pivot_table(index="product",columns="month",values="amount",aggfunc="sum",dropna=False))
print(df.groupby(["product","month"],dropna=False)["amount"].sum(min_count=1).unstack())
print(pd.crosstab(df["product"],df["month"]))
print(pd.crosstab(df["product"],df["month"],dropna=False))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="sum",margins=True,margins_name="Total",dropna=False))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc=f,margins=True,margins_name="Total",dropna=False))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc={"amount":["sum","count"]}))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="count",fill_value=0))
print(df.pivot_table(index="region",columns="month",values="amount",aggfunc="size"))
