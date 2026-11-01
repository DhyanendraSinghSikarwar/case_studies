import math
cases, rule_rate, model_rate, save = 2000, 0.60, 0.75, 150
rule_c, model_c = round(cases * rule_rate), round(cases * model_rate)
extra = model_c - rule_c
print("rules catch", rule_c, "model catches", model_c, "extra", extra, "saving", extra * save)
assert (rule_c, model_c, extra, extra * save) == (1200, 1500, 300, 45_000)
# the 300 is net: it hides overlap. Invented overlap: 1,000 caught by both
both = 1000
rules_only, model_only = rule_c - both, model_c - both
union = both + rules_only + model_only
print("rules-only", rules_only, "model-only", model_only, "net", model_only - rules_only, "union", union)
assert (rules_only, model_only, union) == (200, 500, 1700)
print("model alone loses", rules_only, "cases rules catch =", rules_only * save, "per month")
print("extra saving if ops keeps rules as a layer on top (needs spare review capacity):", (union - rule_c) * save)
assert (union - rule_c) * save == 75_000
# sampling error on 75% of 2,000 and a paired comparison
lo = model_rate - 1.96 * math.sqrt(model_rate * (1 - model_rate) / cases)
hi = model_rate + 1.96 * math.sqrt(model_rate * (1 - model_rate) / cases)
print("95%% interval on model recall: %.3f - %.3f" % (lo, hi))
# McNemar-style on discordant pairs (200 vs 500)
chi = (model_only - rules_only) ** 2 / (model_only + rules_only)
print("discordant-pair chi-square", round(chi, 1))
assert round(chi, 1) == 128.6
