import pandas as pd
ev = pd.DataFrame({"user":[1,1,1,2,2,2,3,3],
                   "item":["a","b","c","a","d","e","b","c"],
                   "ts":pd.to_datetime(["2026-01-01","2026-01-05","2026-01-20","2026-01-02","2026-01-18","2026-01-25","2026-01-03","2026-01-22"])})
cut = pd.Timestamp("2026-01-15")
train, test = ev[ev.ts < cut], ev[ev.ts >= cut]
# evaluate only users seen in train; drop already-consumed items from the ground truth
seen = train.groupby("user")["item"].apply(set)
test = test[test.user.isin(seen.index)]
test = test[[i not in seen[u] for u, i in zip(test.user, test.item)]]
print(test[["user","item"]].to_string(index=False))
