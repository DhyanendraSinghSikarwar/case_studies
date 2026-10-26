import sys, numpy as np, pandas as pd
rng = np.random.default_rng(15)
def frame(n, age_mu, inc_mu, p_city):
    return pd.DataFrame({"age": rng.normal(age_mu, 8, n).round(1),
                         "income": rng.normal(inc_mu, 15000, n).round(0),
                         "city": rng.choice(["Mumbai", "Pune", "Delhi"], n, p=p_city)})
frame(2000, 35, 60000, [.4, .3, .3]).to_csv(sys.argv[1] + "/ref.csv", index=False)
frame(2000, 36, 70000, [.2, .3, .5]).to_csv(sys.argv[1] + "/cur.csv", index=False)
