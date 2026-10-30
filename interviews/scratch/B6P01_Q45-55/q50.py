# Q50: month-over-month retention rises 55% -> 62% while the product is not growing (illustrative)
import pandas as pd

# Two month-to-month transitions. Within each segment, retention is IDENTICAL in both.
RET = {"core": 0.85, "casual": 0.25}
t = {
  "before": dict(base={"core": 50_000, "casual": 50_000}, new=20_000, resurrected=5_000),
  "after":  dict(base={"core": 40_000, "casual": 25_000}, new=8_000,  resurrected=7_000),
}
res = {}
for k, v in t.items():
    base = sum(v["base"].values())
    retained = sum(v["base"][s] * RET[s] for s in RET)
    actives_next = retained + v["new"] + v["resurrected"]
    churned = base - retained
    res[k] = dict(base=base, retained=retained, retention=retained / base, actives_next=actives_next,
                  churned=churned, quick_ratio=(v["new"] + v["resurrected"]) / churned,
                  core_share=v["base"]["core"] / base)
df = pd.DataFrame(res).T
print(df.round(3).to_string())

assert round(res["before"]["retention"], 2) == 0.55 and round(res["after"]["retention"], 2) == 0.62
assert res["before"]["retained"] == 55_000 and res["after"]["retained"] == 40_250      # fewer retained PEOPLE
assert res["before"]["actives_next"] == 85_000 and res["after"]["actives_next"] == 55_250
assert round(res["before"]["quick_ratio"], 2) == 0.56 and round(res["after"]["quick_ratio"], 2) == 0.60

# mix-standardised retention: apply the BEFORE mix to the AFTER segment rates
w = {s: t["before"]["base"][s] / 100_000 for s in RET}
std_after = sum(w[s] * RET[s] for s in RET)
print("after, holding last period's mix:", round(std_after, 3), "(unchanged: the rise is pure mix)")
assert round(std_after, 2) == 0.55

# a leaky definition: counting resurrected users in the numerator of "last month's actives"
leak = (res["after"]["retained"] + t["after"]["resurrected"]) / res["after"]["base"]
print("leaky 'retention' with resurrected users in the numerator:", round(leak, 3))
assert round(leak, 3) == 0.727
