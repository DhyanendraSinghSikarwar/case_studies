import pandas as pd
df = pd.DataFrame({"loan_id": [1, 2, 3, 4, 5], "age": [25, 40, None, 17, 130], "status": ["open", "closed", "open", "paid", "open"]})
errs = []
if df.age.isna().any(): errs.append(("non-null age", df.index[df.age.isna()].tolist()))
bad = df[df.age.notna() & ~df.age.between(18, 100)]
if len(bad): errs.append(("age range 18-100", bad.index.tolist()))
bad = df[~df.status.isin(["open", "closed"])]
if len(bad): errs.append(("status allowed", bad.index.tolist()))
if len(df) < 100: errs.append(("row count >= 100", [len(df)]))
for e in errs: print(e)
