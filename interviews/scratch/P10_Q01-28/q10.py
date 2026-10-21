import pandas as pd
d = pd.DataFrame({"seg": ["mobile", "mobile", "desktop", "desktop"],
                  "arm": ["A", "B", "A", "B"],
                  "users": [4000, 1000, 1000, 4000],
                  "conv": [400, 95, 300, 1140]})
d["rate"] = d.conv / d.users
print(d)
t = d.groupby("arm")[["users", "conv"]].sum()
print(t.conv / t.users)
